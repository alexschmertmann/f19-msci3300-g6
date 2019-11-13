# f19-msci3300-g6
Group 6 repository for South Liberty Public Library project

Create Table Materials
USE f19_msci3300;
CREATE TABLE group7_materials(
MaterialID int(11) NOT NULL AUTO_INCREMENT,
MaterialClass varchar(25) NOT NULL,
CallNumber varchar(255) NOT NULL,
Title varchar(255) NOT NULL,
Author varchar(255),
Publisher varchar(255) NOT NULL,
Copyright int(4),
ISBN int(15) NOT NULL,
DateAdded DATETIME NOT NULL,
LastModified DATETIME NOT NULL,
)ENGINE=InnoDB AUTO_INCREMENT;