#!/usr/bin/env python3

c = b"AZBQCEDTEXFHGOHLIMJFKKLDMVNNOUPBQWRYSGTIUPVAWCXJYRZS"

target = [
    0x52,
    0x55,
    0x45,
    0x43,
    0x4B,
    0x57,
    0x41,
    0x45,
    0x52,
    0x54,
    0x53,
    0x49,
    0x4E,
    0x47,
    0x45,
    0x4E,
    0x49,
    0x45,
    0x55,
    0x52,
    0x57,
    0x45,
    0x53,
    0x45,
    0x4E]

d = {}

for i in range(0, len(c), 2):
    d[c[i]] = c[i + 1]


out = bytearray()
for v in target:
    out.append(d[v])

print(bytes(out))

"""
sc = {0x47, 0x66, 0x1E, 0x87, 0x9D, 0xEC, 0x4C, 0x90, 0x9B, 0xD9, 0xD1, 0xA0, 0x4F, 0x39, 0x31, 0x9E, 0x63, 0x33, 0xFD, 0xBA, 0x01, 0x2D, 0x9A, 0xBF, 0x04, 0x09, 0xB7, 0x16, 0x3D, 0xD8, 0x22, 0x5F, 0x53, 0x0B, 0xD9, 0x52, 0x5E, 0xA2, 0x7C, 0x6E, 0xBF, 0x6E, 0x63, 0x00, 0x7F, 0xF5, 0xDF, 0x91, 0xB6, 0x7E, 0xA9, 0xA3, 0xAD, 0x43, 0x88, 0x00, 0x38, 0xFB, 0xEA, 0x77, 0xBC, 0x0D, 0x01, 0x16, 0xD2, 0x7A, 0xF2, 0x11, 0xCA, 0x9B, 0x19, 0x25, 0x20, 0xC9, 0x92, 0xA4, 0x1A, 0x7F, 0x89, 0xF4, 0x43, 0x20, 0x91, 0xBB, 0x07, 0x8B, 0x81, 0x57, 0x6B, 0x37, 0x41, 0x95, 0x42, 0x2B, 0x46, 0xCF, 0xE2, 0x79, 0xB7, 0xCB, 0x20, 0x7A, 0x0D, 0x8E, 0x65, 0xD2, 0x65, 0x7B, 0x93, 0x80, 0x5D, 0x24, 0x9D, 0xA9, 0x60, 0x9A, 0x61, 0x06, 0xE7, 0xCD, 0xD2, 0x4D, 0x94, 0xFD, 0xB9, 0xE9, 0x1B, 0xF0, 0x5F, 0x87, 0x43, 0x75, 0xCE, 0x96, 0x0A, 0x45, 0x03, 0x33, 0x50, 0x26, 0xF7, 0xEE, 0x5F, 0x2A, 0x57, 0x62, 0x55, 0x86, 0x99, 0xB9, 0xC5, 0x7E, 0xA8, 0xBC, 0x84, 0xA4, 0x0B, 0xCC, 0x37, 0xE9, 0xEF, 0xD8, 0x6B, 0x74, 0xA6, 0xA8, 0x8C, 0xDF, 0xC9, 0x9A, 0x96, 0x45, 0xDD, 0xF1, 0xBA, 0x3B, 0x66, 0x74, 0xB1, 0xFB, 0xD7, 0xCA, 0xB7, 0x5D, 0xE7, 0x9F, 0xE3, 0xF4, 0x93, 0xFE, 0x35, 0xA2, 0xC8, 0x19, 0xBC, 0xCB, 0x3D, 0xC2, 0xBF, 0xC6, 0xFF, 0x13, 0x2B, 0x20, 0x2C, 0x93, 0x79, 0x99, 0xCB, 0x25, 0x1E, 0x35, 0x3A, 0xA6, 0x26, 0x52, 0xD1, 0xDB, 0x04, 0x97, 0x01, 0x30, 0x6F, 0x1B, 0xEB, 0x25, 0xB1, 0x02, 0x85, 0xC2, 0x05, 0x27, 0x5C, 0xB0, 0x0C, 0x56, 0xA0, 0xB2, 0x14, 0x49, 0x04, 0x07, 0x0D, 0x41, 0x22, 0xFD, 0x8D, 0x58, 0x0C, 0xE3, 0xB8, 0xD9, 0x94, 0x26, 0xD6, 0xF9, 0xD2, 0x3D, 0xA0, 0x61, 0x58, 0x09, 0x45, 0xB0, 0x51, 0x74, 0x53, 0x0E, 0x98, 0x63, 0x4A, 0xE1, 0x25, 0x24, 0xE4, 0xDD, 0x35, 0x05, 0x1F, 0xAD, 0x7F, 0x48, 0x04, 0x76, 0x63, 0x1B, 0x6F, 0x52, 0xAA, 0x5C, 0xAC, 0x3B, 0xB3, 0xC9, 0xD6, 0x7A, 0x56, 0xA8, 0xD8, 0x4F, 0x2A, 0xBE, 0x65, 0xBE, 0x85, 0xA9, 0xAD, 0x9F, 0x4A, 0x34, 0xD1, 0x96, 0x4B, 0x1A, 0xA9, 0x24, 0xCB, 0x05, 0x6A, 0x34, 0x79, 0xD0, 0x4F, 0x3D, 0x67, 0xC4, 0xC0, 0x79, 0xD1, 0xDB, 0x23, 0x54, 0x4B, 0xA9, 0x52, 0x2A, 0x43, 0xBE, 0xB5, 0xD6, 0x97, 0xEB, 0x31, 0x0B, 0x9C, 0x4C, 0x4A, 0x9A, 0x51, 0xAC, 0x91, 0xBD, 0x18, 0xD1, 0x22, 0x1C, 0x85, 0xA1, 0x0C, 0xCE, 0x6F, 0x1A, 0x49, 0xB3, 0x06, 0xFF, 0xD9, 0xC3, 0x62, 0x2A, 0xE5, 0x79, 0x29, 0x46, 0x24, 0xB2, 0xDD, 0x32, 0xB3, 0x07, 0xFD, 0x89, 0xE7, 0x02, 0xDB, 0x46, 0xDE, 0xD1, 0x1B, 0x2C, 0x3C, 0xE4, 0xCE, 0x56, 0xF3, 0x6B, 0x27, 0xC7, 0xD5, 0x2D, 0x8C, 0x0F, 0x3D, 0x13, 0x1C, 0x34, 0x28, 0xA3, 0x9B, 0x54, 0xE9, 0xA2, 0x46, 0x13, 0xD6, 0x0F, 0xE7, 0xB1, 0xED, 0x7D, 0xA2, 0x51, 0x89, 0xB0, 0xC1, 0xC6, 0x4F, 0x00, 0x45, 0xE8, 0xD9, 0x66, 0x6E, 0x59, 0x37, 0x3F, 0x4B, 0x07, 0x97, 0xF1, 0xAE, 0x83, 0x20, 0xD7, 0x1C, 0xF2, 0x2B, 0x24, 0x22, 0x33, 0xD3, 0xE6, 0xC7, 0x29, 0x6E, 0x76, 0x1E, 0x6A, 0x35, 0x1C, 0x7E, 0x14, 0xE3, 0xF5, 0x47, 0x50, 0x22, 0x61, 0x73, 0x9F, 0xB5, 0x61, 0x94, 0x2A, 0xF8, 0x9A, 0x1B, 0x5E, 0xBE, 0x74, 0x2A, 0x9E, 0x7C, 0xB1, 0x0E, 0xB5, 0x8B, 0x2D, 0xED, 0xD3, 0xA7, 0x9A, 0xA2, 0xEF, 0xE4, 0x73, 0xF8, 0xF3, 0x7F, 0x13, 0xC9, 0xF3, 0x18, 0x8C, 0xC7, 0xCC, 0x4F, 0xD3, 0x01, 0xA0, 0x2F, 0xB3, 0x40, 0xDB, 0x05, 0x3F, 0xBC, 0x74, 0xF8, 0x48, 0xE8, 0xD6, 0x5D, 0x89, 0xE8, 0xC0, 0x06, 0x8A, 0x24, 0x69, 0x7F, 0x8A, 0x42, 0xE9, 0xEA, 0x0E, 0x86, 0xFF, 0xD4, 0xEF, 0xF8, 0xB3, 0x0B, 0xFD, 0x90, 0x34, 0x7B, 0x2D, 0x0E, 0x73, 0x5C, 0xE7, 0x52, 0xA2, 0x66, 0x1A, 0x52, 0xD6, 0xB5, 0x8E, 0xB8, 0x2B, 0x9A, 0x7D, 0xEB, 0x2C, 0x68, 0x87, 0x4A, 0x74, 0x3D, 0xDC, 0x13, 0x98, 0xC7, 0xF7, 0x45, 0x0F, 0xAF, 0x3A, 0xDA, 0x5A, 0xF1, 0xC1, 0x09, 0xE8, 0x5C, 0x86, 0x18, 0x8B, 0xDA, 0x6F, 0xDA, 0xC6, 0x6A, 0xBE, 0x39, 0xF8, 0xCF, 0xE6, 0xF0, 0xBB, 0x96, 0xED, 0xD9, 0xD4, 0x0C, 0xF2, 0x87, 0x56, 0xEC, 0x6D, 0x22, 0xA0, 0x51, 0xF5, 0xAB, 0xBA, 0xD3, 0x39, 0xCD, 0x96, 0xE9, 0x68, 0x96, 0xB6, 0x98, 0x2E, 0x9C, 0xC8, 0x9D, 0x84, 0xE5, 0x14, 0x44, 0x27, 0xE0, 0x12, 0xE0, 0xC4, 0x60, 0x09, 0x66, 0x4D, 0x19, 0x45, 0x22, 0xF5, 0x63, 0x55, 0x06, 0xB7, 0x59, 0xF8, 0xFA, 0x8A, 0xC4, 0xA1, 0xE0, 0x1F, 0x64, 0x67, 0xE9, 0xBF, 0x2E, 0xAD, 0x5E, 0x7A, 0xB4, 0x91, 0x23, 0xFF, 0x49, 0x1D, 0x1B, 0xCA, 0xAF, 0xA4, 0x8F, 0x71, 0xAA, 0xE6, 0xAE, 0x6F, 0x25, 0xC3, 0x5F, 0xAC, 0xD6, 0x60, 0x85, 0x8A, 0xA2, 0x20, 0x3C, 0x95, 0x82, 0x1F, 0xD9, 0x17, 0xA3, 0xBF, 0x19, 0xCF, 0x7B, 0x86, 0xAA, 0xD0, 0x87, 0x01, 0x94, 0x17, 0x30, 0x7F, 0x00, 0x9D, 0xEC, 0xDB, 0x1E, 0x6B, 0xC4, 0x82, 0xF7, 0x0B, 0x75, 0x92, 0x0E, 0x23, 0x88, 0x4D, 0x3D, 0x4A, 0xD6, 0x9B, 0x7B, 0xD7, 0x62, 0x6F, 0x55, 0xDF, 0xFE, 0x9C, 0x1C, 0xDB, 0x00, 0xF4, 0x2F, 0x25, 0x6E, 0xE4, 0xC5, 0x0E, 0x41, 0x8F, 0xA9, 0xE4, 0xBF, 0xFE, 0xAE, 0x8C, 0x82, 0x9C, 0x1B, 0x5B, 0x5F, 0xE4, 0xAC, 0x43, 0x62, 0xD2, 0x6F, 0xCE, 0xA2, 0xE8, 0x05, 0x85, 0x35, 0xA2, 0x0D, 0x08, 0xD1, 0xA6, 0x11, 0x1C, 0xF2, 0xE5, 0x47, 0xD1, 0xB7, 0x31, 0x9E, 0xCF, 0x01, 0x1B, 0xF1, 0x09, 0x46, 0x06, 0x15, 0xBE, 0x49, 0x5C, 0x0F, 0x63, 0xF8, 0x47, 0xF2, 0x8C, 0x04, 0x8E, 0x95, 0xA4, 0x0E, 0xB8, 0xCF, 0x05, 0xAC, 0xE3, 0x14, 0x22, 0x18, 0xAC, 0xB6, 0x71, 0x6C, 0x22, 0x2E, 0x9C, 0xD1, 0xD7, 0xD6, 0x21, 0x8F, 0xAD, 0x7C, 0x6A, 0xA9, 0x5E, 0x34, 0x5B, 0x8F, 0xA8, 0x46, 0xA0, 0x54, 0xC7, 0x51, 0x6D, 0xF7, 0x4A, 0x30, 0x5B, 0x28, 0x00, 0x87, 0x88, 0x83, 0x55, 0xA1, 0x43, 0x94, 0xC5, 0xB3, 0x95, 0xC2, 0x19, 0xA1, 0x26, 0xC7, 0xB7, 0xE2, 0xFC, 0x66, 0xBE, 0x41, 0x15, 0xB8, 0xB6, 0xF8, 0x15, 0xCA, 0x76, 0x68, 0x41, 0x85, 0x31, 0xFE, 0x78, 0x63, 0xF5, 0x3A, 0x51, 0x62, 0x72, 0xE8, 0xEA, 0xEE, 0x33, 0x36, 0xB7, 0xD9, 0x98, 0xD3, 0x2A, 0xAA, 0xD5, 0x13, 0x0C, 0x19, 0x16, 0x21, 0x1D, 0xB2, 0xE3, 0xD9, 0x63, 0x89, 0x33, 0x66, 0xC9, 0x41, 0x81, 0xE8, 0xF8, 0x1F, 0x40, 0x56, 0x3B, 0x80, 0x32, 0x1B, 0x94, 0xC0, 0xBB, 0xDB, 0x51, 0xC3, 0x25, 0xA6, 0xA0, 0xB1, 0x3C, 0x7F, 0x1C, 0x91, 0x5A, 0xB0, 0x98, 0xF3, 0x3D, 0x00, 0x2C, 0x26, 0x46, 0x44, 0x36, 0x67, 0x33, 0x0C, 0x0C};
"""
