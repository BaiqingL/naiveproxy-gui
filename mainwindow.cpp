#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QDebug>
#include <QtGlobal>
#include <QJsonDocument>
#include <QJsonObject>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_actionExit_triggered()
{
    QApplication::quit();
}

void MainWindow::on_actionLoad_config_triggered()
{
    QString configName = QFileDialog::getOpenFileName(this,
                                                    tr("Open naive configuration file"), "",
                                                    tr("JSON File (*.json)"));
    QFile configFile(configName);

    try {
        // Open file, read data and convert to QString
        configFile.open(QIODevice::ReadOnly | QIODevice::Text);
        QString configValues = configFile.readAll();
        configFile.close();
        QJsonObject configObject = QJsonDocument::fromJson(configValues.toUtf8()).object();
        QString proxyPort = configObject.take(QString ("listen")).toString();
        QString allOtherData = configObject.take(QString ("proxy")).toString().remove(0,8);

        // Set proxy port
        ui->proxyEntry->setPlainText(proxyPort.remove(0,proxyPort.size() - 4));

        // Set user value
        QString userName = allOtherData.leftRef(allOtherData.indexOf(":")).toString();
        ui ->usernameEntry->setPlainText(userName);

        allOtherData.remove(0, allOtherData.indexOf(":") + 1);

        // Set password value
        QString password = allOtherData.leftRef(allOtherData.lastIndexOf("@")).toString();
        ui ->passwordEntry->setPlainText(password);

        allOtherData.remove(0, allOtherData.indexOf("@") + 1);

        // Set server value
        ui->serverAddressEntry->setPlainText(allOtherData);
    } catch (...) {
        // Any error handling
        QMessageBox messageBox;
        messageBox.critical(0,"Error","Error occured trying to open file");
    }
}

void MainWindow::on_actionExport_config_triggered()
{
    //qDebug() << ui->passwordEntry->toPlainText().length();
    if (ui->serverAddressEntry->toPlainText().length() && ui->usernameEntry->toPlainText().length() && ui->passwordEntry->toPlainText().length() && ui->proxyEntry->toPlainText().length()){
        QString saveTarget = QFileDialog::getSaveFileName(this,
                                                          tr("Save naive configuration file"), "",
                                                          tr("JSON File (*.json)"));

        // Construct json configuration file
        QJsonObject naiveConfig;
        naiveConfig.insert("listen", QJsonValue("socks://127.0.0.1:" + ui->proxyEntry->toPlainText()));
        naiveConfig.insert("proxy", QJsonValue("https://" + ui->usernameEntry->toPlainText() + ":" + ui->passwordEntry->toPlainText() + "@" + ui->serverAddressEntry->toPlainText()));
        naiveConfig.insert("padding", QJsonValue(true));
        QJsonDocument configDoc(naiveConfig);

        // Save to file
        QFile jsonFile(saveTarget);
        jsonFile.open(QFile::WriteOnly);
        jsonFile.write(configDoc.toJson());

    } else {
        QMessageBox messageBox;
        messageBox.critical(0,"Not enough parameters","Not all parameters are filled");
    }

}

void MainWindow::on_actionConnect_triggered()
{
    if (ui->serverAddressEntry->toPlainText().length() && ui->usernameEntry->toPlainText().length() && ui->passwordEntry->toPlainText().length() && ui->proxyEntry->toPlainText().length()){

    } else {
        QMessageBox messageBox;
        messageBox.critical(0,"Not enough parameters","Not all parameters are filled");
    }
}
