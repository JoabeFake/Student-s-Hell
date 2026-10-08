import pygame
import engine

logical_width = 320
logical_height = 360
# viewport_width = 1280
# viewport_height = 720

# scale_x = 1
# scale_y = 1

# pixel_width = 1
# pixel_height = 1

surface = None
surface_width = 0
surface_height = 0

logical_surface = None

clipping = None

def set_logical_surface(new_surface):
    global logical_surface
    logical_surface = new_surface

def get_logical_surface():
    return logical_surface

def set_surface(new_surface):
    global surface
    global surface_width
    global surface_height
    global logical_surface

    surface = new_surface
    surface_width = surface.get_width()
    surface_height = surface.get_height()
    logical_surface = pygame.Surface((logical_width, logical_height))

def janelaViewport(janela, viewport):
    Wxmin, Wymin, Wxmax, Wymax = janela
    Vxmin, Vymin, Vxmax, Vymax = viewport

    largura_janela = Wxmax - Wxmin
    altura_janela = Wymax - Wymin

    largura_viewport = Vxmax - Vxmin
    altura_viewport = Vymax - Vymin

    if largura_janela == 0 or altura_janela == 0:
        return engine.identity()

    sx = largura_viewport / largura_janela
    sy = altura_viewport / altura_janela

    matriz = engine.identity()

    # Move a janela para a origem
    matriz = engine.multiply_matrixes(
        engine.translation(-Wxmin, -Wymin),
        matriz
    )

    # Escala a janela para o tamanho do viewport
    matriz = engine.multiply_matrixes(
        engine.scale(sx, sy),
        matriz
    )

    # Move para a posição do viewport
    matriz = engine.multiply_matrixes(
        engine.translation(Vxmin, Vymin),
        matriz
    )

    return matriz

def criarJanelaZoom(
    centro_x,
    centro_y,
    largura,
    altura,
    zoom
):
    if zoom <= 0:
        zoom = 1

    largura_janela = largura / zoom
    altura_janela = altura / zoom

    xmin = centro_x - largura_janela / 2
    ymin = centro_y - altura_janela / 2

    xmax = centro_x + largura_janela / 2
    ymax = centro_y + altura_janela / 2

    return (
        xmin,
        ymin,
        xmax,
        ymax
    )

def transformViewport(points, window, viewport):
    matrix = janelaViewport(
        window,
        viewport
    )

    return engine.transform_polygon(
        points,
        matrix
    )

def criarViewport(
    x,
    y,
    largura,
    altura
):
    return (
        x,
        y,
        x + largura,
        y + altura
    )

def criarViewportMinimapa(
    x,
    y,
    largura,
    altura
):
    return criarViewport(
        x,
        y,
        largura,
        altura
    )

def desenharPoligonoViewport(
    vertices,
    color,
    janela,
    viewport,
    surface=None,
    preencher=True
):
    if surface is None:
        surface = logical_surface

    vertices_transformados = transformViewport(
        vertices,
        janela,
        viewport
    )

    if preencher:
        drawPolygonFill(
            vertices_transformados,
            color,
            surface
        )
    else:
        drawPolygon(
            vertices_transformados,
            color,
            surface
        )

def desenharTexturaViewport(
    pontos,
    uvs,
    textura,
    janela,
    viewport,
    surface=None
):
    if surface is None:
        surface = logical_surface

    pontos_transformados = transformViewport(
        pontos,
        janela,
        viewport
    )

    scanlineTexture(
        pontos_transformados,
        uvs,
        textura,
        surface
    )

def desenharTexturaCompletaViewport(
    textura,
    janela,
    viewport,
    surface=None
):
    if surface is None:
        surface = logical_surface

    largura = janela[2] - janela[0]
    altura = janela[3] - janela[1]

    pontos = [
        (janela[0], janela[1]),
        (janela[0] + largura, janela[1]),
        (janela[0] + largura, janela[1] + altura),
        (janela[0], janela[1] + altura)
    ]

    tex_w = textura.get_width()
    tex_h = textura.get_height()

    u_min = janela[0] / tex_w
    v_min = janela[1] / tex_h
    
    u_max = janela[2] / tex_w
    v_max = janela[3] / tex_h

    uvs = [
        (u_min, v_min),
        (u_max, v_min),
        (u_max, v_max),
        (u_min, v_max)
    ]

    desenharTexturaViewport(
        pontos,
        uvs,
        textura,
        janela,
        viewport,
        surface
    )

def limitarJanela(janela, limite):
    xmin, ymin, xmax, ymax = janela

    limite_xmin, limite_ymin, limite_xmax, limite_ymax = limite

    largura = xmax - xmin
    altura = ymax - ymin

    largura_limite = limite_xmax - limite_xmin
    altura_limite = limite_ymax - limite_ymin

    # A janela não pode ser maior que o mundo
    if largura > largura_limite:
        largura = largura_limite

    if altura > altura_limite:
        altura = altura_limite

    # Limite esquerdo
    if xmin < limite_xmin:
        xmin = limite_xmin
        xmax = xmin + largura

    # Limite direito
    if xmax > limite_xmax:
        xmax = limite_xmax
        xmin = xmax - largura

    # Limite superior
    if ymin < limite_ymin:
        ymin = limite_ymin
        ymax = ymin + altura

    # Limite inferior
    if ymax > limite_ymax:
        ymax = limite_ymax
        ymin = ymax - altura

    return (
        xmin,
        ymin,
        xmax,
        ymax
    )

def definirClipping(xmin, ymin, xmax, ymax):
    global clipping

    clipping = (
        int(xmin),
        int(ymin),
        int(xmax),
        int(ymax)
    )

def removerClipping():
    global clipping

    clipping = None

def setPixel(x, y, color, surface=None):
    global clipping

    if surface is None:
        surface = logical_surface

    x, y = int(x), int(y)

    if not (0 <= x < surface.get_width() and
            0 <= y < surface.get_height()):
        return

    if clipping is not None:
        xmin, ymin, xmax, ymax = clipping

        if (x < xmin or
            x > xmax or
            y < ymin or
            y > ymax):
            return

    surface.set_at((x, y), color)

def setPixelAlpha(x, y, color, surface=None):
    global clipping

    if surface is None:
        surface = logical_surface

    x, y = int(x), int(y)

    if not (0 <= x < surface.get_width() and
            0 <= y < surface.get_height()):
        return

    if clipping is not None:
        xmin, ymin, xmax, ymax = clipping

        if (x < xmin or
            x > xmax or
            y < ymin or
            y > ymax):
            return

    if len(color) < 4:
        surface.set_at((x, y), color)
        return

    r, g, b, a = color

    # Totalmente transparente
    if a == 0:
        return

    # Totalmente opaco
    if a == 255:
        surface.set_at(
            (x, y),
            (r, g, b)
        )
        return

    # Alfa parcial
    fundo = surface.get_at((x, y))

    fr, fg, fb = fundo[:3]

    alpha = a / 255.0

    nr = int(
        r * alpha +
        fr * (1 - alpha)
    )

    ng = int(
        g * alpha +
        fg * (1 - alpha)
    )

    nb = int(
        b * alpha +
        fb * (1 - alpha)
    )

    surface.set_at(
        (x, y),
        (nr, ng, nb)
    )

def getPixel(x, y):
    if (x < 0 or x >= logical_width) or (y < 0 or y >= logical_height):
        return (0, 0, 0)
    
    return tuple(logical_surface.get_at((x, y)))

def interpolate_color(c1, c2, t):
    r = int(c1[0] + (c2[0] - c1[0]) * t)
    g = int(c1[1] + (c2[1] - c1[1]) * t)
    b = int(c1[2] + (c2[2] - c1[2]) * t)

    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))

    return (r, g, b)

def scanlineFillGradient(points, colors):
    ys = [p[1] for p in points]
    y_min = int(min(ys))
    y_max = int(max(ys))

    n = len(points)

    for y in range(y_min, y_max):
        intersections = []

        for i in range(n):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % n]

            c0 = colors[i]
            c1 = colors[(i + 1) % n]

            if y0 == y1:
                continue

            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                c0, c1 = c1, c0

            if y < y0 or y >= y1:
                continue

            t = (y - y0) / (y1 - y0)
            x = x0 + t * (x1 - x0)
            color_y = interpolate_color(c0, c1, t)

            intersections.append((x, color_y))

        intersections.sort(key = lambda i: i[0])

        for i in range(0, len(intersections), 2):
            if i + 1 < len(intersections):
                x_ini, color_ini = intersections[i]
                x_end, color_end = intersections[i + 1]

                if x_end == x_ini:
                    continue

                for x in range(int(x_ini), int(x_end) + 1):
                    t = (x - x_ini) / (x_end - x_ini)
                    color = interpolate_color(color_ini, color_end, t)
                    setPixel(x, y, color)

def drawBresenhamLine(x1, y1, x2, y2, color, surface=None):
    x1 = int(x1)
    y1 = int(y1)
    y2 = int(y2)
    x2 = int(x2)

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = -1 if x1 > x2 else 1
    sy = -1 if y1 > y2 else 1

    error = dx - dy

    x, y = x1, y1

    while True:
        setPixel(x, y, color, surface)

        if x == x2 and y == y2:
            break

        e2 = 2 * error

        if e2 > -dy:
            error -= dy
            x += sx
        
        if e2 < dx:
            error += dx
            y += sy

def drawPolygon(vertices, color, surface=None):
    n = len(vertices)
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        drawBresenhamLine(x1, y1, x2, y2, color, surface)

def scanlineFill(vertices, color, surface=None):
    ys = [p[1] for p in vertices]

    if surface is None:
        surface = logical_surface

    y_min = max(0, int(min(ys)))

    y_max = min(surface.get_height() - 1, int(max(ys)))

    n = len(vertices)

    for y in range(y_min, y_max + 1):
        intersections = []

        for i in range(n):
            x0, y0 = vertices[i]
            x1, y1 = vertices[(i + 1) % n]

            if y0 == y1:
                continue

            if y0 > y1:
                x0, y0, x1, y1 = (
                    x1, y1,
                    x0, y0
                )

            if y < y0 or y >= y1:
                continue

            x = (x0 + (y - y0) * (x1 - x0) / (y1 - y0))

            intersections.append(x)

        intersections.sort()

        for i in range(0, len(intersections), 2):
            if i + 1 < len(intersections):
                x_begin = int(intersections[i])

                x_end = int(intersections[i + 1])

                for x in range(x_begin, x_end + 1):
                    setPixel(x, y, color, surface)

def drawPolygonFill(vertices, color, surface=None):
    drawPolygon(vertices, color, surface)
    scanlineFill(vertices, color, surface)

def drawRectangle(x, y, width, height, color, surface=None):
    line_x = x + width
    line_y = y + height

    vertices = [(x, y), (line_x, y), (line_x, line_y), (x, line_y)]

    drawPolygon(vertices, color, surface)

def drawRectFillSL(x, y, width, height, color, surface=None):
    drawRectangle(x, y, width, height, color, surface)
    line_x = x + width
    line_y = y + height

    vertices = [(x, y), (line_x, y), (line_x, line_y), (x, line_y)]
    drawPolygonFill(vertices, color, surface)
    
def drawBresenhamCircle(xc, yc, radius, color):
    x, y = 0, radius
    d = 3 - 2 * radius

    drawCircle(xc, yc, x, y, color)

    while(y >= x):
        if(d > 0):
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6
        x += 1

        drawCircle(xc, yc, x, y, color)

def drawCircleFill(xc, yc, radius, color):
    drawBresenhamCircle(xc, yc, radius, color)
    floodFillDFS(xc, yc, color)

def drawCircleFillSL(xc, yc, radius, color, surface=None):
    x, y = 0, radius
    d = 3 - 2 * radius
    
    fillCircle(xc, yc, x, y, color, surface)

    while(y >= x):
        if(d > 0):
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6
        x += 1

        fillCircle(xc, yc, x, y, color, surface)

def fillCircle(xc, yc, x, y, color, surface=None):
    drawHorizontalLine(xc - x, xc + x, yc + y, color, surface)
    drawHorizontalLine(xc - x, xc + x, yc - y, color, surface)

    drawHorizontalLine(xc - y, xc + y, yc + x, color, surface)
    drawHorizontalLine(xc - y, xc + y, yc - x, color, surface)

def drawHorizontalLine(x1, x2, y, color, surface=None):
    for x in range(round(x1), round(x2 + 1)):
        setPixel(x, y, color, surface)

def drawCircle(xc, yc, x, y, color):
    setPixel(xc + x, yc + y, color)
    setPixel(xc - x, yc + y, color)
    setPixel(xc + x, yc - y, color)
    setPixel(xc - x, yc - y, color)

    setPixel(xc + y, yc + x, color)
    setPixel(xc - y, yc + x, color)
    setPixel(xc + y, yc - x, color)
    setPixel(xc - y, yc - x, color)

def dfs(x, y, oldColor, newColor):
    surface = pygame.display.get_surface()

    if(x < 0 or x >= surface.get_width() or
       y < 0 or y >= surface.get_height()):
        return
    
    if(getPixel(x, y) != oldColor):
        return
    
    setPixel(x, y, newColor)

    dfs(x + 1, y, oldColor, newColor)
    dfs(x - 1, y, oldColor, newColor)
    dfs(x, y + 1, oldColor, newColor)
    dfs(x, y - 1, oldColor, newColor)

def floodFillDFS(sx, sy, newColor):
    oldColor = getPixel(sx, sy)

    if(oldColor == newColor):
        return
    
    dfs(sx, sy, oldColor, newColor)

def drawRectFill(x, y, width, height, color):
    drawRectangle(x, y, width, height, color)
    floodFillDFS(x + width//2, y + height//2, color)

def nearestNeighbor(texture, u, v):
    width = texture.get_width()
    height = texture.get_height()

    u = max(0, min(1, u))
    v = max(0, min(1, v))

    x = round(u * (width - 1))
    y = round(v * (height - 1))

    return tuple(texture.get_at((x, y)))

def scanlineTexture(pontos, uvs, textura, surface=None):

    if surface == None:
        surface = logical_surface

    n = len(pontos)

    ys = [p[1] for p in pontos]

    y_min = int(min(ys))
    y_max = int(max(ys))

    tex_width = textura.get_width()
    tex_height = textura.get_height()

    for y in range(y_min, y_max):

        intersecoes = []

        for i in range(n):

            x0, y0 = pontos[i]
            x1, y1 = pontos[(i + 1) % n]

            u0, v0 = uvs[i]
            u1, v1 = uvs[(i + 1) % n]

            if y0 == y1:
                continue

            if y0 > y1:
                x0, y0 = x1, y1
                x1, y1 = pontos[i]

                u0, v0 = u1, v1
                u1, v1 = uvs[i]

            if y < y0 or y >= y1:
                continue

            t = (y - y0) / (y1 - y0)

            x = x0 + t * (x1 - x0)

            u = u0 + t * (u1 - u0)
            v = v0 + t * (v1 - v0)

            intersecoes.append((x, u, v))

        intersecoes.sort(key=lambda item: item[0])

        for i in range(0, len(intersecoes), 2):

            if i + 1 >= len(intersecoes):
                continue

            x_ini, u_ini, v_ini = intersecoes[i]
            x_fim, u_fim, v_fim = intersecoes[i + 1]

            if x_fim == x_ini:
                continue

            for x in range(int(x_ini), int(x_fim) + 1):

                t = (x - x_ini) / (x_fim - x_ini)

                u = u_ini + t * (u_fim - u_ini)
                v = v_ini + t * (v_fim - v_ini)

                cor = nearestNeighbor(
                    textura,
                    u,
                    v
                )

                setPixelAlpha(x, y, cor, surface)