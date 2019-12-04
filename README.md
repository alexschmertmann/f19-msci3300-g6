# f19-msci3300-g6
Group 6 repository for South Liberty Public Library modernization project. The application allows librarians to add/update/search/delete materials to/from the catalog and add/update/search/delete patron accounts. Given a material id and patron id, users can checkout materials from the catalog.

DEVELOPERS
Lakota Larson, lakota-larson@uiowa.edu
Alex Schmertmann, alex-schmertmann@uiowa.edu
Chengze Weng, chengze-weng@uiowa.edu
Zhehuan Zhang, zhehuan-zhang@uiowa.edu



SYNTAX FOR CREATE TABLES:

Create Table Materials
CREATE TABLE group7_materials(
	MaterialID int(11) NOT NULL AUTO_INCREMENT,
	MaterialClass varchar(25),
	CallNumber varchar(255),
	Title varchar(255) ,
	Author varchar(255),
	Publisher varchar(255),
	Copyright int(4),
	ISBN int(15) ,
	DateAdded DATETIME,
	LastModified DATETIME ,
PRIMARY KEY (MaterialID)
)ENGINE=InnoDB AUTO_INCREMENT=1;

USE f19_msci3300;

CREATE TABLE group7_patrons(
	patronId int(11) NOT NULL AUTO_INCREMENT,
	firtName varchar(255) NOT NULL,
	lastName varchar(255) NOT NULL,
	birthdate DATE NOT NULL,
	address1 varchar(255),
	address2 varchar(255),
	city varchar(255) NOT NULL,
	state char(2) NOT NULL,
	zip int(5) NOT NULL,
	phoneNumber1 int(10),
	phoneNumber2 int(10),
	email varchar(255),
PRIMARY KEY ('patronId')
) ENGINE =InnoDB AUTO_INCREMENT =1;

CREATE TABLE group7_circulation(
	checkoutId int(11) NOT NULL AUTO_INCREMENT,
	materialId int(11) NOT NULL,
	patronId int(11) NOT NULL,
	dayRented DATE NOT NULL,
	dueDate DATE NOT NULL,
PRIMARY KEY ('checkoutId')
FOREIGN KEY (materialId) REFERENCES group7_materials(materialId)
FOREIGN KEY (patronId) REFERENCES group7_patrons(patronId)
) ENGINE =InnoDB AUTO_INCREMENT =1
;
