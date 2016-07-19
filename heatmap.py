
import sys
import plotly.plotly as py
from plotly.tools import FigureFactory as FF
import plotly.graph_objs as go
import os
import json
import pandas as pd


Identify genes/branch lengths of interest
calculate pearson
calculate pvalue
heatmap in plotly

############################################
##calculates Pearson coefficient on a matrix of branch lengths across multiple genes
##argv[1]is .txt file with list of gene names
############################################


def chooseGenes():
	with open("fam_dict.txt","r") as t:
		fam_dict=json.load(t)
		
		
	return(gene_list, cladeNum)




##works
def makeStudyDict(gene_list, cladeNum):
	with open("gene_dict.txt","r") as t:
		gene_dict=json.load(t)
	study_dict={}
	x=[]
	for gene in gene_list:
		v=gene_dict[gene]
		clade=v[cladeNum]
		for i in clade:
			i_list=[t.strip() for t in i.split()]
			study_dict[i_list[0]]=i_list[1:]
			x.append(i_list[0])
	y=x	
	return(study_dict,x,y)



#works
def calcPearson(study_dict):
	df=pd.DataFrame.from_dict(study_dict,"columns",float)
	pearson=df.corr()
	pearson=pearson.round(3)
	return(pearson)
	

def makeHeatMap(pearson,x,y):
	#Set colorscale:
	colorscale=[[0, 'rgb(166,206,227)'], [0.25, 'rgb(31,120,180)'], [0.45, 'rgb(178,223,138)'], [0.65, 'rgb(51,160,44)'], [0.85, 'rgb(251,154,153)'], [1, 'rgb(227,26,28)']]
	#Get matrix from pandas style:
	z=pearson.values.tolist()
	#Reverse matrix:
	z = z[::-1]
	x = x[::-1]
	#Create heatmap:
	fig = FF.create_annotated_heatmap(z, x=x, y=y, colorscale="colorscale")
	#View figure:
	py.iplot(fig, filename='annotated_heatmap')
	
	

def calculatePearson():
	genes=open(sys.argv[1], "r")
	genelist = [x.strip() for x in genes.readlines()]
	length_dict={}
	
	samplegene=genelist[0]
	samplefile=open(samplegene+"_branchlengths.txt", "r")
	samplel=samplefile.readlines()
	s=samplel[0]
	branches=[t.strip() for t in s.split()]
	samplefile.close()
	
	for item in genelist:
		pamlfile=open(item+"_branchlengths.txt", "r")	
		lines=pamlfile.readlines()
		l=lines[1]
		length=[t.strip() for t in l.split()]
		length_dict[item]=length
		pamlfile.close()
	df=pd.DataFrame.from_dict(length_dict,'columns',float)
	df.index=branches
	pearson=df.corr()
	#print (pearson)
	sys.stdout.write(pearson)
############################################
calculatePearson()



with open("working_dict.txt","r") as t:
	working_dict=json.load(t)
with open("fam_dict.txt","r") as g:
	fam_dict=json.load(g)

with open("fam_dict.txt", "w") as outfile:
	json.dump(fam_dict,outfile)
