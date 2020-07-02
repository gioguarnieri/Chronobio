# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 17:30:20 2020

@author: Giovanni G Soares
"""
import sys
from PyQt5.QtWidgets import QWidget, QInputDialog, QFileDialog, \
    QLabel, QApplication, QMessageBox
from PyQt5.QtGui import QPixmap
import csv
import statistics
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


# Classes to the GUI

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 input dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        # Setting up the windows
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # Standard threshold as no
        self.Thresh = "No"
        # Getting the files to work on them
        self.namefile = self.openFileNamesDialog()
        # Is it a temperature or activity file?
        self.column = self.getInteger()
        # starting the lists to store the data
        ldata, lhora, ldado, fullfile = [], [], [], []
        # making the lists with hour, date and data
        ldata, lhora, ldado, header, fullfile = self.mkList(self.namefile,
                                                            self.column)
        # Naming the output compiled data
        namefile = "HumansCompiledColumn{}".format(self.column)
        self.writeFile(ldado, fullfile, header, namefile)
        # Making the histogram with the data
        # getting a suggestion to threshold values
        self.vlThreshmax, self.vlThreshmin = self.mkHisto(self.column, ldado)
        # Plotting the original data, without modification
        self.plotData(ldata, ldado, self.vlThreshmin, self.vlThreshmax,
                      self.column, self.Thresh, namefile)
        image = '{}histo.png'.format(self.column)
        # Showing the histogram to the user
        pixmap = QPixmap(image)
        self.showGraph(pixmap)
        # If it is a temperature file, give the user a option to a threshold
        self.vlThreshmin, self.vlThreshmax, Thresh = self.ifThresh(
            self.vlThreshmin, self.vlThreshmax)
        if Thresh:
            # getting the values to threshold
            # self.vlThreshmin, self.vlThreshmax=self.getDouble()
            # applying the threshold
            ldata, lhora, ldado = self.applyThresh(ldata, lhora,
                                                   ldado, self.vlThreshmin,
                                                   self.vlThreshmax)
            # Making another histogram to show the user
            self.mkHisto(str(self.column) + "Thresh", ldado)
            image = '{}histo.png'.format("Thresh")
            pixmap = QPixmap(image)
            # Showing the histogram
            self.showGraph(pixmap)
            namefile = "Threshold" + namefile
            self.writeFile(ldado, fullfile, header, namefile)
            # writing the data
            self.plotData(ldata, ldado, self.vlThreshmin, self.vlThreshmax,
                          self.column, self.Thresh, namefile)
            # Plotting the new thresholded data
        if self.ifSmooth():
            w1, w2, w3 = self.getWeight()
            ldado = self.suaviza(ldado, w1, w2, w3)
            namefile = "Smooth" + namefile
            self.writeFile(ldado, fullfile, header, namefile)
            self.plotData(ldata, ldado, self.vlThreshmin, self.vlThreshmax,
                          self.column, self.Thresh, namefile)
        if self.ifDetrend():
            ldado = self.detrend(ldado)
            namefile = "Detrend" + namefile
            self.writeFile(ldado, fullfile, header, namefile)
            self.plotData(ldata, ldado, self.vlThreshmin, self.vlThreshmax,
                          self.column, self.Thresh, namefile)
        ldata, lhora, ldado = self.hrlyMean(ldata, lhora, ldado)
        self.writeFilemean(ldata, lhora, ldado, "HrlyMeanColumn{}.txt"
                           .format(self.column))
        namefile = "Hrlymean" + namefile
        self.plotData(ldata, ldado, self.vlThreshmin, self.vlThreshmax,
                      self.column, self.Thresh, namefile)

    # Just some GUI stuff, pretty self explanatory

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                "All Files (*);;Python Files (*.py)", options=options)
        if files:
            return files

    def writeFilemean(self, ldata, lhora, ldado, namefile):
        filewrite = open(namefile, "w")
        for i in range(0, len(ldado)):
            if str(ldado[i]) != "nan":
                filewrite.write("{}\t{}\t{}\n".format(ldata[i], lhora[i], ldado[i]))
            else:
                filewrite.write("{}\t{}\n".format(ldata[i], lhora[i]))
        filewrite.close()

    def getInteger(self):
        i, okPressed = QInputDialog.getInt(self, "Get column", "Column", 6, 0, 100, 1)
        if okPressed:
            return i

    def getDouble(self):
        d, okPressed = QInputDialog.getDouble(self, "Value to threshold", "Minimun value:", self.vlThreshmin, 0, 100, 3)
        e, okPressed = QInputDialog.getDouble(self, "Value to threshold", "Maximun value:", self.vlThreshmax, 0, 100, 3)
        if okPressed:
            return d, e

    def getWeight(self):
        w1, okPressed = QInputDialog.getDouble(self, "Weight to middle value", "Weight to first value:", 1.0, 0, 100,
                                               10)
        w2, okPressed = QInputDialog.getDouble(self, "Weight to middle value", "Weight to second value:", 1.0, 0, 100,
                                               10)
        w3, okPressed = QInputDialog.getDouble(self, "Weight to middle value", "Weight to third value:", 1.0, 0, 100,
                                               10)
        if okPressed:
            return w1, w2, w3

    def ifThresh(self, mini, maxi):
        buttonReply = QMessageBox.question(self, '',
                                           "Use {0:.3} and {1:.3} as min and max threshold?\n Cancel to not use threshold"
                                           .format(
                                               mini, maxi), QMessageBox.Yes |
                                           QMessageBox.No | QMessageBox.Cancel,
                                           QMessageBox.Yes)
        if buttonReply == QMessageBox.Yes:
            return mini, maxi, True
        if buttonReply == QMessageBox.No:
            d, okPressed = QInputDialog.getDouble(self, "", "Minimun value:",
                                                  mini, 0, 100, 3)
            e, okPressed = QInputDialog.getDouble(self, "", "Maximun value:",
                                                  maxi, 0, 100, 3)
            if okPressed:
                return d, e, True
        if buttonReply == QMessageBox.Cancel:
            return mini, maxi, False

    def ifSmooth(self):
        buttonReply = QMessageBox.question(self, '', "Smooth the data?",
                                           QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.Yes)
        if buttonReply == QMessageBox.Yes:
            return True
        if buttonReply == QMessageBox.No:
            return False

    def ifDetrend(self):
        buttonReply = QMessageBox.question(self, '', "Detrend the data?",
                                           QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.Yes)
        if buttonReply == QMessageBox.Yes:
            return True
        if buttonReply == QMessageBox.No:
            return False

    def showGraph(self, pixmap):
        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        self.show()

    def mkList(self, filenames, column):
        ldado = []
        ldata = []
        lhora = []
        fullfile = []
        for nomes in filenames:
            # opening the file
            csv_file = open(nomes, "r")
            # setting the delimiter to , and reading it
            csv_reader = csv.reader(csv_file, delimiter=';')
            header = ""
            for i in next(csv_reader):
                header = header + i + ", "
            header = header[:-1]
            header = header + "\n"
            # jumping the header
            # getting the data
            for lines in csv_reader:
                # if there is nan in the line it will change how many ,
                # and how many data, so we have to make a distinction
                data, hora, dado = lines[0].split(" ")[0],lines[0].split(" ")[1][:5], lines[column - 1]
                ldado.append(float(dado))
                ldata.append(data)
                lhora.append(hora)
                linhaw = lines[0]
                for i in range(1, len(lines)):
                    if i == column - 1:
                        linhaw = linhaw + ", {}"
                    else:
                        linhaw = linhaw + "," + lines[i]
                linhaw = linhaw + '\n'
                fullfile.append(linhaw)
        return ldata, lhora, ldado, header, fullfile

    # just applies the threshold in a limite the user puts in the box
    def applyThresh(self, ldata, lhora, ldado, vlThreshmin, vlThreshmax):
        newlhora = []
        newldado = []
        newldata = []
        for i in range(0, len(ldado)):
            if vlThreshmin <= ldado[i] <= vlThreshmax:
                newlhora.append(lhora[i]), newldado.append(ldado[i]),
                newldata.append(ldata[i])
            else:
                newlhora.append(lhora[i]), newldado.append(np.nan),
                newldata.append(ldata[i])
        return newldata, newlhora, newldado

    # smoothing the data with weighted values
    def suaviza(self, ldado, w1, w2, w3):
        newldado = []
        for i in range(1, len(ldado) - 1):
            newldado.append((w1 * ldado[i - 1] + w2 * ldado[i] + w3 *
                             ldado[i + 1]) / (w1 + w2 + w3))
        return newldado

    # writing on a file the data, skipping values with NaN
    def writeFile(self, ldado, fullfile, header, namefile):
        filewrite = open(namefile + ".txt", "w")
        filewrite.write(str(header))
        for i in range(0, len(ldado)):
            if str(ldado[i]) != "nan":
                filewrite.write(fullfile[i].format(ldado[i]))
            else:
                filewrite.write(fullfile[i].format("  "))
        filewrite.close()

    # plotting the data
    def plotData(self, ldata, ldado, vlThreshmin, vlThreshmax, tipo, ifThresh, nomegrafico):
        SMALL_SIZE = 15
        MEDIUM_SIZE = 18
        BIGGER_SIZE = 20
        keys = [[], []]
        # making keys to the graph xtics
        for i in ldata:
            if i not in keys[0]:
                keys[0].append(i)
                # it counts how many times a certain date appears in the list,
                # knowing how many data there is in it so we can
                # show the xtics with an accurate spacing
                keys[1].append(ldata.count(keys[0][-1]))

        eixoX = np.zeros(len(keys[1]))
        # sum of how much time has passed for each xtic
        for i in range(1, len(keys[1])):
            eixoX[i] = eixoX[i - 1] + keys[1][i - 1]
        # just plotting now
        plt.figure(num=None, figsize=(45, 12), dpi=100, facecolor='w', edgecolor='k')
        plt.rc('font', size=BIGGER_SIZE)  # controls default text sizes
        # plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
        # plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
        # plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
        # plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
        plt.grid(color="gray", linestyle="dotted", linewidth=2)
        plt.xticks(eixoX, keys[0], rotation=45)
        if ifThresh == "No":
            plt.title("Graph relating the date and the {} column".format(tipo))
        else:
            plt.title("Graph relating the date and the {} column,\n Threshold Min={} Threshold Max={}".format(tipo,
                                                                                                              vlThreshmin,
                                                                                                              vlThreshmax))
        plt.ylabel(tipo)
        plt.xlabel("Date")
        plt.plot(range(0, len(ldado)), ldado, color="red")
        plt.savefig(nomegrafico + ".png", bbox_inches="tight")
        plt.cla()

    def mkHisto(self, tipo, ldado):
        lista = []
        for i in ldado:
            if str(i) != "nan":
                lista.append(i)
        plt.figure(num=None, figsize=(20, 12), dpi=100, facecolor='w',
                   edgecolor='k')
        plt.xlabel("{} value".format(tipo))
        plt.ylabel("Frequency")
        # calculating the outliers, which is the mean plus or minus two times the standard deviation
        mean = sum(lista) / len(lista)
        sdev = statistics.stdev(lista)
        outliermenos = mean - 2 * sdev
        outliermais = mean + 2 * sdev
        plt.title("{0} histogram, media +/- 2sd={1:2.5}+/-{2:2.5}"
                  .format(tipo, mean, 2 * sdev))
        count, bins, ignored = plt.hist(ldado, 50, density=False)
        plt.savefig("{}histo.png".format(tipo), bbox_inches="tight")
        return outliermais, outliermenos

    def detrend(self, ldado):
        data = np.array(ldado)
        data = data[~np.isnan(data)]
        m, b, r_val, p_val, std_err = stats.linregress(range(0, len(data)),
                                                       data)
        newldado = []
        x = 0
        for i in ldado:
            if str(i) != "nan":
                newldado.append(i - m * x)
            else:
                newldado.append(np.nan)
            x = x + 1
        return newldado

    def hrlyMean(self, ldata, lhora, ldado):
        hrlyMeandado = []
        hrlyMeanhora = []
        hrlyMeandata = []
        k = 0
        while (str(ldado[k]) == "nan"):
            k += 1
        old = lhora[k][:2]
        sumdado = 0
        count = 0
        for i in range(k, len(ldado)):
            if str(ldado[i]) != "nan":
                if lhora[i][:2] == old:
                    sumdado = sumdado + ldado[i]
                    count += 1
                else:
                    hrlyMeandado.append(sumdado / count)
                    sumdado = ldado[i]
                    count = 1
                    hrlyMeanhora.append(old + ":30:00")
                    old = lhora[i][:2]
                    hrlyMeandata.append(ldata[i - 1])
        return hrlyMeandata, hrlyMeanhora, hrlyMeandado


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    ex = App()
