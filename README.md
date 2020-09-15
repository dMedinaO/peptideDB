## DOCUMENTOS Y DIRECTORIOS

En este repositorio, se encuentran almacenadas distintas familias de péptidos, relacionadas con el virus VIH. A partir de estas familias, se realizan diferentes analisis que permiten identificar motivos conservados, estudiar el largo de las secuencias y las tendencias/preferencias de residuos. Además, se estudian las propiedades descritas en la base de datos AAIndex, las cuales son empleadas para codificar las secuencias de peptidos en diccionarios numéricos.

## Directorios y contenido

La disposición de los directorios y su contenido se explica a continuación:

## 1. Scripts

Directorio que permite almacenar los scripts implementados para desarrollar los diferentes análisis. Todos los scripts se encuentran implementados bajo lenguaje de programación Python, en su versión 2.7 y se apoya de librerías como Numpy, Pandas y Scikit-Learn para la manipulación de conjuntos de datos.

## 2. Inputs

Directorio que almacena archivo con información general de los péptidos y familias. Dentro de este directorio, se encuentra la base de datos AAIndex, en su formato procesada, esta base de datos se emplea para futuras codificaciones de secuencias lineales, identificación de propiedades relevantes, entre otras.

## 3. Results

Directorio que almacena los resultados de todos los análisis generados. Presenta los siguientes subdirectorios:

- Aligments: Directorio con los resultados de alineamiento empleando Clustal Omega, por cada tipo de familia, se almacena un archivo multifasta con el resultado del alineamiento.

- AligmentsInCSVFormat: Directorio con los resultados de los alineamientos, en formato CSV, analizando la tendencia en porcentaje  del residuo o gap existente en cada posición. Además, genera un archivo resumen con la secuencia consenso en base a la mayor tendencia por posición.

- FastaFiles: Representan las secuencias en formato fasta, las cuales se extraen desde los archivos xlsx.

- PCAAnalysis: Representa los análisis de PCA generados a las propiedades de la base de datos AAIndex. Los análisis se dividen en dos: conjuntos estandarizados y no estandarizados. En cada uno de ellos, se realizan análisis con respecto al porcentaje de varianza a analizar, el cual varia en [85, 90, 95, 97.5], para cada uno de estos, se obtiene un shape de los componentes para los residuos, lo cual permite codificar residuos en formato componentes y se entrega un resumen de la contribución/aporte a la varianza de cada componente. También, se encuentra un gráfico resumen de número de componentes v/s porcentaje de varianza representado, esto permite identificar cuántas componentes son necesarias para obtener un % representativo deseado.
