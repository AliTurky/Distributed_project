# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import image_processing_pb2 as image__processing__pb2

GRPC_GENERATED_VERSION = '1.63.0'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in image_processing_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class ImageProcessingStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ProcessImageChunk = channel.unary_unary(
                '/imageprocessing.ImageProcessing/ProcessImageChunk',
                request_serializer=image__processing__pb2.ImageChunk.SerializeToString,
                response_deserializer=image__processing__pb2.ImageChunk.FromString,
                _registered_method=True)
        self.ProcessImage = channel.unary_unary(
                '/imageprocessing.ImageProcessing/ProcessImage',
                request_serializer=image__processing__pb2.ProcessImageRequest.SerializeToString,
                response_deserializer=image__processing__pb2.ProcessImageResponse.FromString,
                _registered_method=True)
        self.ProcessImages = channel.unary_unary(
                '/imageprocessing.ImageProcessing/ProcessImages',
                request_serializer=image__processing__pb2.ProcessImagesRequest.SerializeToString,
                response_deserializer=image__processing__pb2.ProcessImagesResponse.FromString,
                _registered_method=True)


class ImageProcessingServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ProcessImageChunk(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ProcessImage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ProcessImages(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ImageProcessingServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ProcessImageChunk': grpc.unary_unary_rpc_method_handler(
                    servicer.ProcessImageChunk,
                    request_deserializer=image__processing__pb2.ImageChunk.FromString,
                    response_serializer=image__processing__pb2.ImageChunk.SerializeToString,
            ),
            'ProcessImage': grpc.unary_unary_rpc_method_handler(
                    servicer.ProcessImage,
                    request_deserializer=image__processing__pb2.ProcessImageRequest.FromString,
                    response_serializer=image__processing__pb2.ProcessImageResponse.SerializeToString,
            ),
            'ProcessImages': grpc.unary_unary_rpc_method_handler(
                    servicer.ProcessImages,
                    request_deserializer=image__processing__pb2.ProcessImagesRequest.FromString,
                    response_serializer=image__processing__pb2.ProcessImagesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'imageprocessing.ImageProcessing', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ImageProcessing(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ProcessImageChunk(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/imageprocessing.ImageProcessing/ProcessImageChunk',
            image__processing__pb2.ImageChunk.SerializeToString,
            image__processing__pb2.ImageChunk.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ProcessImage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/imageprocessing.ImageProcessing/ProcessImage',
            image__processing__pb2.ProcessImageRequest.SerializeToString,
            image__processing__pb2.ProcessImageResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ProcessImages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/imageprocessing.ImageProcessing/ProcessImages',
            image__processing__pb2.ProcessImagesRequest.SerializeToString,
            image__processing__pb2.ProcessImagesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)