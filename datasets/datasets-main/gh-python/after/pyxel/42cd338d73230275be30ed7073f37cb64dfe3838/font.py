from .image import Image

MIN_FONT_CODE = 32
MAX_FONT_CODE = 127

FONT_WIDTH = 4
FONT_HEIGHT = 6
FONT_IMAGE_WIDTH = FONT_WIDTH * 16
FONT_IMAGE_HEIGHT = FONT_HEIGHT * 6
FONT_IMAGE_ROW_COUNT = FONT_IMAGE_WIDTH // FONT_WIDTH

FONT_DATA = [
    0x000000,
    0x444040,
    0xaa0000,
    0xaeaea0,
    0x6c6c40,
    0x824820,
    0x4a4ac0,
    0x440000,
    0x244420,
    0x844480,
    0xa4e4a0,
    0x04e400,
    0x000480,
    0x00e000,
    0x000040,
    0x224880,
    0x6aaac0,
    0x4c4440,
    0xc248e0,
    0xc242c0,
    0xaae220,
    0xe8c2c0,
    0x68eae0,
    0xe24880,
    0xeaeae0,
    0xeae2c0,
    0x040400,
    0x040480,
    0x248420,
    0x0e0e00,
    0x842480,
    0xe24040,
    0x4aa860,
    0x4aeaa0,
    0xcacac0,
    0x688860,
    0xcaaac0,
    0xe8e8e0,
    0xe8e880,
    0x68ea60,
    0xaaeaa0,
    0xe444e0,
    0x222a40,
    0xaacaa0,
    0x8888e0,
    0xaeeaa0,
    0xcaaaa0,
    0x4aaa40,
    0xcac880,
    0x4aae60,
    0xcaeca0,
    0x6842c0,
    0xe44440,
    0xaaaa60,
    0xaaaa40,
    0xaaeea0,
    0xaa4aa0,
    0xaa4440,
    0xe248e0,
    0x644460,
    0x884220,
    0xc444c0,
    0x4a0000,
    0x0000e0,
    0x840000,
    0x06aa60,
    0x8caac0,
    0x068860,
    0x26aa60,
    0x06ac60,
    0x24e440,
    0x06ae24,
    0x8caaa0,
    0x404440,
    0x2022a4,
    0x8acca0,
    0xc444e0,
    0x0eeea0,
    0x0caaa0,
    0x04aa40,
    0x0caac8,
    0x06aa62,
    0x068880,
    0x06c6c0,
    0x4e4460,
    0x0aaa60,
    0x0aaa40,
    0x0aaee0,
    0x0a44a0,
    0x0aa624,
    0x0e24e0,
    0x64c460,
    0x444440,
    0xc464c0,
    0x6c0000,
    0xeeeee0,
]


def create_font_image():
    image = Image(FONT_IMAGE_WIDTH, FONT_IMAGE_HEIGHT)
    row_count = FONT_IMAGE_WIDTH // FONT_WIDTH

    for i, v in enumerate(FONT_DATA):
        left = (i % row_count) * FONT_WIDTH
        top = (i // row_count) * FONT_HEIGHT
        data = image.data

        for j in range(FONT_WIDTH * FONT_HEIGHT):
            x = left + j % FONT_WIDTH
            y = top + j // FONT_WIDTH
            data[y, x] = 1 if v & 0x800000 else 0
            v <<= 1

    return image
