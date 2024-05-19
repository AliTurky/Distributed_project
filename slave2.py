import grpc
from concurrent import futures
import image_processing_pb2
import image_processing_pb2_grpc
import cv2
import numpy as np
from io import BytesIO
from PIL import Image

class ImageProcessingServicer(image_processing_pb2_grpc.ImageProcessingServicer):
    def ProcessImageChunk(self, request, context):
        image_np = np.frombuffer(request.data, dtype=np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        # Perform chosen processing option
        processing_option = request.processing_option
        if processing_option == "grayscale":
            processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        elif processing_option == "canny":
            # Implement Canny edge detection
            processed_image = cv2.Canny(image, 100, 200)
        elif processing_option == "blue":
            # Placeholder for blue processing
            processed_image = image  # Placeholder
        else:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Invalid processing option")
            return image_processing_pb2.ImageChunk()

        # Encode processed image to bytes
        _, encoded_image = cv2.imencode('.jpg', processed_image)
        encoded_bytes = encoded_image.tobytes()

        # Create response
        return image_processing_pb2.ImageChunk(data=encoded_bytes)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    image_processing_pb2_grpc.add_ImageProcessingServicer_to_server(ImageProcessingServicer(), server)
    server.add_insecure_port('slave2 privateIP:50051')
    server.start()
    print("slave 2 is listening...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
