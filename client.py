import grpc
import image_processing_pb2
import image_processing_pb2_grpc
import cv2
import numpy as np
from tkinter import filedialog, Tk, Label, Button, OptionMenu, StringVar, messagebox, Text, simpledialog,END
from PIL import Image, ImageTk

# Define the server address
server_address_list = ['master1 IP','master2 IP']

def is_server_available(server_address_list):
    available_servers = []
    for server_address in server_address_list:
        try:
            channel = grpc.insecure_channel(server_address)
            grpc.channel_ready_future(channel).result(timeout=1)
            available_servers.append(server_address)
        except grpc.FutureTimeoutError:
            continue
    return available_servers

def send_image(image_data, processing_option):
    available_servers = is_server_available(server_address_list)
    if available_servers:
        chosen_server = available_servers[0]  # Default to the first available server
        if len(available_servers) > 1:
            chosen_server = simpledialog.askstring("Choose master Server", "Available Servers: " + ", ".join(available_servers), initialvalue=available_servers[0])
            if chosen_server not in available_servers:
                messagebox.showwarning("Warning", "Invalid server address. Using the default server.")
                chosen_server = available_servers[0]
        try:
            # Open a gRPC channel
            channel = grpc.insecure_channel(chosen_server)

            # Create a stub (client)
            stub = image_processing_pb2_grpc.ImageProcessingStub(channel)

            # Create a request object
            request = image_processing_pb2.ProcessImageRequest(image_data=image_data, processing_option=processing_option)

            # Call the remote method
            response = stub.ProcessImage(request)

            # Decode the processed image
            processed_image_np = np.frombuffer(response.processed_image, dtype=np.uint8)
            processed_image = cv2.imdecode(processed_image_np, cv2.IMREAD_COLOR)

            return processed_image, response.logs
        except grpc.RpcError as e:
            print(f"Error: {e}")
    else:
        messagebox.showwarning("Warning", "No master servers available.")
    return None, []

def send_images(image_data_list, processing_option):
    available_servers = is_server_available(server_address_list)
    if available_servers:
        chosen_server = available_servers[0]  # Default to the first available server
        if len(available_servers) > 1:
            chosen_server = simpledialog.askstring("Choose master Server", "Available Servers: " + ", ".join(available_servers), initialvalue=available_servers[0])
            if chosen_server not in available_servers:
                messagebox.showwarning("Warning", "Invalid server address. Using the default server.")
                chosen_server = available_servers[0]
        try:
            # Open a gRPC channel
            channel = grpc.insecure_channel(chosen_server)

            # Create a stub (client)
            stub = image_processing_pb2_grpc.ImageProcessingStub(channel)

            # Create a request object
            request = image_processing_pb2.ProcessImagesRequest(
                images=[image_processing_pb2.ImageData(image_data=image_data, processing_option=processing_option)
                        for image_data in image_data_list]
            )

            # Call the remote method
            response = stub.ProcessImages(request)

            # Decode the processed images
            processed_images = []
            for image_data in response.processed_images:
                processed_image_np = np.frombuffer(image_data.image_data, dtype=np.uint8)
                processed_image = cv2.imdecode(processed_image_np, cv2.IMREAD_COLOR)
                processed_images.append(processed_image)

            return processed_images, response.logs
        except grpc.RpcError as e:
            print(f"Error: {e}")
    else:
        messagebox.showwarning("Warning", "No master servers available.")
    return None, []

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing App")
        self.root.geometry("600x400")  # Set window size

        # Set background image
        self.background_image = Image.open("5221116.jpg")
        self.background_image = self.background_image.resize((600, 400))
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = Label(root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.label = Label(root, text="Choose images and processing option:", bg="white", font=("Arial", 16))
        self.label.pack(pady=10)

        self.upload_button = Button(root, text="Upload Images", command=self.upload_images, bg="purple", fg="white", font=("Arial", 12))
        self.upload_button.pack(pady=5)

        self.options = ["canny", "grayscale", "blue"]
        self.processing_option = StringVar(root)
        self.processing_option.set(self.options[0])

        self.option_menu = OptionMenu(root, self.processing_option, *self.options)
        self.option_menu.pack(pady=5)

        self.process_button = Button(root, text="Process Images", command=self.process_images, bg="black", fg="white", font=("Arial", 12))
        self.process_button.pack(pady=5)

        self.logs_text = Text(root, height=10, width=60, bg="lightgray", font=("Arial", 10))
        self.logs_text.pack(pady=10)

        self.images_paths = []

    def upload_images(self):
        self.images_paths = filedialog.askopenfilenames()
        if self.images_paths:
            messagebox.showinfo("Info", f"Selected {len(self.images_paths)} images.")
        else:
            messagebox.showwarning("Warning", "No files selected.")

    def process_images(self):
        self.logs_text.delete(1.0, END)  # Clear previous logs
        if not self.images_paths:
            messagebox.showwarning("Warning", "No images to process. Please upload images first.")
            return

        processing_option = self.processing_option.get()
        if len(self.images_paths) == 1:
            image_path = self.images_paths[0]
            # Read image as numpy array
            image_np = cv2.imread(image_path)

            # Encode image as bytes
            _, encoded_image = cv2.imencode('.jpg', image_np)
            image_data = encoded_image.tobytes()

            processed_image, logs = send_image(image_data, processing_option)

            if processed_image is not None:
                cv2.imshow('Processed Image', processed_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                self.display_logs(logs)
            else:
                messagebox.showerror("Error", "Failed to process the image.")
        else:
            image_data_list = []
            for image_path in self.images_paths:
                # Read image as numpy array
                image_np = cv2.imread(image_path)

                # Encode image as bytes
                _, encoded_image = cv2.imencode('.jpg', image_np)
                image_data = encoded_image.tobytes()
                image_data_list.append(image_data)

            processed_images, logs = send_images(image_data_list, processing_option)

            if processed_images is not None:
                for i, processed_image in enumerate(processed_images):
                    cv2.imshow(f'Processed Image {i + 1}', processed_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                self.display_logs(logs)
            else:
                messagebox.showerror("Error", "Failed to process the images.")

    def display_logs(self, logs):
        for log in logs:
            self.logs_text.insert(END, log + "\n")

def main():
    root = Tk()
    app = ImageProcessingApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
