"""Darknet19 Model Defined in Keras."""
import sys
import functools
from functools import partial

from keras.layers import Convolution2D, MaxPooling2D
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.normalization import BatchNormalization
from keras.models import Model
from keras.regularizers import l2

sys.path.append('/home/pi/PoochPak/yolo_picam/yad2k/utils/')
from utils import compose

# Partial wrapper for Convolution2D with static default argument.
_DarknetConv2D = partial(Convolution2D, border_mode='same')


@functools.wraps(Convolution2D)
def DarknetConv2D(*args, **kwargs):
    """Wrapper to set Darknet weight regularizer for Convolution2D."""
    darknet_conv_kwargs = {'W_regularizer': l2(5e-4)}
    darknet_conv_kwargs.update(kwargs)
    return _DarknetConv2D(*args, **darknet_conv_kwargs)


def DarknetConv2D_BN_Leaky(*args, **kwargs):
    """Darknet Convolution2D followed by BatchNormalization and LeakyReLU."""
    return compose(
        DarknetConv2D(*args, **kwargs),
        BatchNormalization(),
        LeakyReLU(alpha=0.1))


def bottleneck_block(nb_outer, nb_bottleneck):
    """Bottleneck block of 3x3, 1x1, 3x3 convolutions."""
    return compose(
        DarknetConv2D_BN_Leaky(nb_outer, 3, 3),
        DarknetConv2D_BN_Leaky(nb_bottleneck, 1, 1),
        DarknetConv2D_BN_Leaky(nb_outer, 3, 3))


def bottleneck_x2_block(nb_outer, nb_bottleneck):
    """Bottleneck block of 3x3, 1x1, 3x3, 1x1, 3x3 convolutions."""
    return compose(
        bottleneck_block(nb_outer, nb_bottleneck),
        DarknetConv2D_BN_Leaky(nb_bottleneck, 1, 1),
        DarknetConv2D_BN_Leaky(nb_outer, 3, 3))


def darknet_body():
    """Generate first 18 conv layers of Darknet-19."""
    return compose(
        DarknetConv2D_BN_Leaky(32, 3, 3),
        MaxPooling2D(),
        DarknetConv2D_BN_Leaky(64, 3, 3),
        MaxPooling2D(),
        bottleneck_block(128, 64),
        MaxPooling2D(),
        bottleneck_block(256, 128),
        MaxPooling2D(),
        bottleneck_x2_block(512, 256),
        MaxPooling2D(),
        bottleneck_x2_block(1024, 512))


def darknet19(inputs):
    """Generate Darknet-19 model for Imagenet classification."""
    body = darknet_body()(inputs)
    logits = DarknetConv2D(1000, 1, 1)(body)
    return Model(inputs, logits)
