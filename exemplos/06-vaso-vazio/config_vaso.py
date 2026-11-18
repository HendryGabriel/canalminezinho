"""Coordenadas unicas (SET) compartilhadas entre construcao do cenario, elenco e takes."""

Y = 64          # nivel base da ilha verde
MAR = 62        # nivel do oceano
YP = 68         # piso interno do Salao do Palacio Imperial (sobre terraco nobre)
YJ = 65         # piso do Jardim / Varanda da Casa do Ping

SET = {
    'canvas': (1290, -1530, 1550, -1250),          # ilha inteira 260x280 sobre o oceano
    'palacio_box': (1392, -1482, 1448, -1426),     # Grande Palacio Imperial Vermelho e Dourado
    'salao_centro': (1420, 68, -1452),             # centro do tapete vermelho no salao
    'trono': (1420, 70, -1471),                    # trono dourado elevado ao norte (olha para +z / sul)
    'fila_z': -1448,                               # linha Z onde os jovens ficam perfilados (x = 1411, 1415, 1419, 1423)
    'cozinha': (1456, 68, -1456),                  # ala lateral real da panela fervendo as sementes
    'jardim_box': (1390, -1362, 1450, -1308),      # jardim florido + lago koi + cerejeiras + casa do Ping
    'casa_centro': (1420, 65, -1322),              # casa/pavilhao de madeira do Ping
    'janela': (1420, 66, -1328),                   # janela frontal com peitoril onde fica o vaso (vista de fora olhando -z/+z)
    'varanda_mesa': (1414, 65, -1332),             # bancada ensolarada na varanda para regar/tomar sol/por terra
    'canteiro_sol': (1426, 65, -1340),             # ponto aberto no jardim florido com cerejeiras ao fundo
}
