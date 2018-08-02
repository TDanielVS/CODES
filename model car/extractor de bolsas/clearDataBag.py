import glob, os, argparse
import csv


def filterData(file=None):
    indices = []

    for line in file:
        vals = line.split('-')
        if vals.__len__() > 1:
            segm = []
            for i, dato in enumerate(vals):
                segm.append(int(dato))

            for j in range(segm[0], segm[1] + 1, 1):  # Genera el rango de valores
                indices.append(j)

        else:
            indices.append(int(vals[0]))  # Agrega un valor simple

    ## Limpia CSV
    csv_file_name = "datosBolsa.csv"
    lista_data_csv = list()
    f = open(csv_file_name, 'r')

    try:
        reader = csv.reader(f)
        reader = list(reader)

        lista_data_csv.append(reader[0])
        for ind, dat in enumerate(indices):
            cad = reader[dat]
            lista_data_csv.append(cad)

    except:
        print "Error"
        return 1

    finally:
        f.close()

    f = open(csv_file_name, 'wt')
    writer = csv.writer(f)
    for dato in lista_data_csv:
        writer.writerow(dato)

    f.close()

    ## Limpia imagenes
    path = "imagenesBolsa"
    prefix = "image_raw_"

    if os.path.exists(path):
        lista = os.listdir(path)  # Lista archivos de la carpeta path
        number_files = len(lista)  # Numero de Archivos en directorio
        num_ceros = len(str(number_files))
        os.chdir(path + "/")  # Cambio de directorio

        for i in range(1, number_files + 1, 1):  # Remover los archivos que no esten en la lista indices[]

            if i != indices[0]:  # Borrar si no esta en la lista
                name = prefix + str(i).rjust(num_ceros, '0') + "*"

                try:
                    name = str(glob.glob(name)[0])
                    os.remove(name)
                except OSError:
                    print "No se pudo borrar " + name
            else:
                if indices.__len__() > 1:
                    indices.pop(0)
    else:
        print "No existe la carpeta /" + path
        return 1

    print "Los datos se han limpiado :)"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name')  # Args = file_name
    args = parser.parse_args()
    file = open(args.file_name, 'r')

    filterData(file)
