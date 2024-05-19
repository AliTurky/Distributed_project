import grpc
import image_processing_pb2
import image_processing_pb2_grpc
import cv2
import numpy as np
from concurrent import futures

# List of server addresses
SERVER_ADDRESSES = ['3.90.235.175:50051','100.24.68.178:50051','18.212.215.42:50051']  # Add more addresses as needed

def split_image(image):
    height, width, _ = image.shape
    mid_height = height // 2
    chunk1 = image[:mid_height, :]
    chunk2 = image[mid_height:, :]
    return [chunk1, chunk2]

def process_image_chunk(image_chunk, server_address, processing_option):
    try:
        # Create a channel to the server
        channel = grpc.insecure_channel(server_address)
        stub = image_processing_pb2_grpc.ImageProcessingStub(channel)

        # Encode image chunk to bytes
        _, encoded_chunk = cv2.imencode('.jpg', image_chunk)
        encoded_bytes = encoded_chunk.tobytes()

        # Create request
        request = image_processing_pb2.ImageChunk(data=encoded_bytes, processing_option=processing_option)

        # Call gRPC method
        response = stub.ProcessImageChunk(request)

        # Decode processed image from response
        processed_image_np = np.frombuffer(response.data, dtype=np.uint8)
        processed_image = cv2.imdecode(processed_image_np, cv2.IMREAD_COLOR)

        return processed_image
    except grpc.RpcError:
        return None

class ImageProcessingServicer(image_processing_pb2_grpc.ImageProcessingServicer):

    def ProcessImage(self, request, context):
        logs = []  # Store logs for this request
        try:
            # Decode the image from request
            image_np = np.frombuffer(request.image_data, dtype=np.uint8)
            image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

            # Split the image into chunks
            image_chunks = split_image(image)

            processed_image_chunks = []

            available_servers = [server_address for server_address in SERVER_ADDRESSES if self.is_server_available(server_address)]

            if not available_servers:
                logs.append("No servers are available for processing the image.")
                return image_processing_pb2.ProcessImageResponse(logs=logs)

            logs.append(f"Available servers: {len(available_servers)}")

            for i, chunk in enumerate(image_chunks):
                # Get the next available server in round-robin fashion
                server_address = available_servers.pop(0)
                logs.append(f"Processing chunk {i + 1} on server: {server_address}")
                processed_image = process_image_chunk(chunk, server_address, request.processing_option)
                if processed_image is not None:
                    processed_image_chunks.append(processed_image)
                else:
                    logs.append(f"Server {server_address} failed to process chunk {i + 1}.")
                available_servers.append(server_address)  # Add server back to available list

            if not processed_image_chunks:
                logs.append("No server was able to process the image.")
                return image_processing_pb2.ProcessImageResponse(logs=logs)

            # Concatenate processed image chunks
            processed_image = np.vstack(processed_image_chunks)

            # Encode processed image as bytes
            _, encoded_image = cv2.imencode('.jpg', processed_image)
            processed_image_bytes = encoded_image.tobytes()

            # Create a response
            response = image_processing_pb2.ProcessImageResponse(processed_image=processed_image_bytes, logs=logs)

            return response
        except Exception as e:
            logs.append(f"Error: {e}")
            return image_processing_pb2.ProcessImageResponse(logs=logs)

    def ProcessImages(self, request, context):
        logs = []  # Store logs for this request
        try:
            processed_images = []

            available_servers = [server_address for server_address in SERVER_ADDRESSES if self.is_server_available(server_address)]

            if not available_servers:
                logs.append("No servers are available for processing the images.")
                return image_processing_pb2.ProcessImagesResponse(logs=logs)

            logs.append(f"Available servers: {len(available_servers)}")

            server_index = 0
            for image_data in request.images:
                # Decode the image from request
                image_np = np.frombuffer(image_data.image_data, dtype=np.uint8)
                image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

                # Get the next available server in round-robin fashion
                server_address = available_servers[server_index]
                logs.append(f"Processing image on server: {server_address}")
                server_index = (server_index + 1) % len(available_servers)

                processed_image = process_image_chunk(image, server_address, image_data.processing_option)

                if processed_image is not None:
                    # Encode processed image as bytes
                    _, encoded_image = cv2.imencode('.jpg', processed_image)
                    processed_image_bytes = encoded_image.tobytes()

                    processed_images.append(image_processing_pb2.ImageData(image_data=processed_image_bytes,
                                                                          processing_option=image_data.processing_option))
                else:
                    logs.append(f"Server {server_address} failed to process an image.")

            response = image_processing_pb2.ProcessImagesResponse(processed_images=processed_images, logs=logs)
            return response
        except Exception as e:
            logs.append(f"Error: {e}")
            return image_processing_pb2.ProcessImagesResponse(logs=logs)

    def is_server_available(self, server_address):
        try:
            channel = grpc.insecure_channel(server_address)
            grpc.channel_ready_future(channel).result(timeout=1)
            return True
        except grpc.FutureTimeoutError:
            return False

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    image_processing_pb2_grpc.add_ImageProcessingServicer_to_server(ImageProcessingServicer(), server)
    server.add_insecure_port('172.31.31.20:50051')
    server.start()
    print("Master 1 started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
