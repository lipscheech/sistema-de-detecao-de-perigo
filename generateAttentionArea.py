from numpy import ones, tril, flip, uint8

def createAttetionArea(shape, top=150, bottom=230):
    maskCut = ones(shape)
    maskCut = tril(maskCut, 80)
    maskCut = flip(maskCut, -1)
    maskCut = tril(maskCut, 80)
    maskCut[:top, :] = 0
    maskCut[bottom:, :] = 0

    return maskCut.astype(uint8)