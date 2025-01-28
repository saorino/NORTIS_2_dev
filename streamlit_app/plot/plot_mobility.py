import plotly.graph_objects as go
import numpy as np

MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoicHJvamV0b2RhZG9zIiwiYSI6ImNtMXdiOTEydDA1czEyaW41MDYwamIwdGQifQ.CntGc8JTYWf6b9tveFDAVQ"

def plot_mobility(fig, mobility_selected, mobilidade, LINE_MOBILITIES, LINE_COLORS, COLOR_DICT_MOBILITY):
    """
    Adiciona camadas de mobilidade ao mapa Plotly
    
    Args:
        fig: Figura Plotly base
        mobility_selected: Lista de tipos de mobilidade selecionados
        mobilidade: Dicionário com dados de mobilidade
        LINE_MOBILITIES: Lista de tipos de mobilidade que são linhas
        LINE_COLORS: Dicionário de cores para linhas de metrô
        COLOR_DICT_MOBILITY: Dicionário de cores para tipos de mobilidade
    
    Returns:
        fig: Figura Plotly atualizada com as camadas de mobilidade
    """

    tipos_pontuais = []
    if mobility_selected:
        for tipo in mobility_selected:
            df_mobility = mobilidade.get(tipo)
            if df_mobility is not None and not df_mobility.empty:
                if tipo in LINE_MOBILITIES:
                    if tipo in ['Linha metro projeto', 'Linha metro'] and 'lmt_nome' in df_mobility.columns:
                        for nome_linha, grupo in df_mobility.groupby('lmt_nome'):
                            cor_linha = LINE_COLORS.get(nome_linha.upper(), 'blue')
                            line_style = dict(color=cor_linha, width=3)
                            if tipo == 'Linha metro projeto':
                                line_style['dash'] = 'dot'

                            full_lats, full_lons = [], []
                            for geom in grupo.geometry:
                                if geom.geom_type == 'LineString':
                                    coords = list(geom.coords)
                                    lats = [c[1] for c in coords]
                                    lons = [c[0] for c in coords]
                                    if full_lats:
                                        full_lats.append(None)
                                        full_lons.append(None)
                                    full_lats.extend(lats)
                                    full_lons.extend(lons)

                            fig.add_trace(go.Scattermap(
                                lat=full_lats,
                                lon=full_lons,
                                mode='lines',
                                line=line_style,
                                name=f"{tipo} - {nome_linha}",
                                text=f"{tipo}: {nome_linha}",
                                hoverinfo='text',
                                opacity=0.3
                            ))
                    else:
                        default_color = COLOR_DICT_MOBILITY.get(tipo, 'blue')
                        full_lats, full_lons = [], []
                        for geom in df_mobility.geometry:
                            if geom.geom_type == 'LineString':
                                coords = list(geom.coords)
                                lats = [c[1] for c in coords]
                                lons = [c[0] for c in coords]
                                if full_lats:
                                    full_lats.append(None)
                                    full_lons.append(None)
                                full_lats.extend(lats)
                                full_lons.extend(lons)

                        fig.add_trace(go.Scattermap(
                            lat=full_lats,
                            lon=full_lons,
                            mode='lines',
                            line=dict(color=default_color, width=3),
                            name=tipo,
                            text=tipo,
                            hoverinfo='text',
                            opacity=0.3
                        ))
                else:
                    tipos_pontuais.append(tipo)

    markers = {
        'Terminal de onibus': 'aerialway',
        'Estacao de Trem': 'rail',
        'Ponto de onibus': 'bus',
        'Estacao de Metro': 'rail-metro',
    }
    marker_size = {
        'Estacao de Metro': 10,
        'Estacao de Trem': 10,
        'Ponto de onibus': 2,
        'Terminal de onibus': 10,
    }

    for tipo in tipos_pontuais:
        df_mobility = mobilidade.get(tipo)
        if df_mobility is not None and not df_mobility.empty:
            fig.add_trace(go.Scattermap(
                lat=df_mobility['Latitude'],
                lon=df_mobility['Longitude'],
                mode = "markers",
                marker={'size': marker_size[tipo], 'symbol': markers[tipo]},
                name=tipo,
                text=tipo,
                textposition = "bottom right",
                hoverinfo='text',
                opacity=1.0,
                cluster=dict(
                    enabled=False,
                    maxzoom=24
                )
            ))    

    fig.update_layout(
        autosize=True,
        hovermode='closest',
    )

    
    return fig