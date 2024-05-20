# Ser347_2024
Trabalho da disciplina de Introdução Programação -  PGSER/INPE - ano 2024

Instruções de uso dos programas Python para aplicação de realces de imagens por classe de uso da terra.

Autores: Ana Júlia Dias, Andrés Velástegui, Camila Totti, Luis Maurano, Marina Galdez

1) Fazer download das imagens para testes em:
http://www.dpi.inpe.br/prodesdigital/dadostmp/maurano/22668/

2) Descompactar o conteudo do zip em uma pasta.

3) Na mesma pasta usada na descompactação, criar um arquivo em formato texto
com nome: set_path_dir.txt. Este arquivo deverá conter uma única linha
que indique o caminho completo onde estão armazenadas as 
as imagens descompactadas no passo 2. Exemplo: 
/home/Dados/Ser347/22668/

4) Baixar os programas em python.

5) A ordem dos programas a serem executada é:
1. ser347_projeto_normaliza.py: normaliza imagens originias p/ valores entre 0 e 1
2. ser347_projeto_indices.py: gera indices espectrais (NDVI, EVI...)
3. ser347_projeto_cluster.py  : gera imagem clasificada com classes de uso por agrupamento de cluster
4. ser347_projeto_masc_ndvi_cluster.py: gera mascaras das bandas normalizadas por classe d euso
5. ser347_projeto_realce.py: gera imagens realcadas por banda e por classe de uso

