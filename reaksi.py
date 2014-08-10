#!/usr/bin/python2

# development stage

import argparse
import os
from array import array
argh = argparse.ArgumentParser(description='Meramalkan suatu reaksi kimia')
argh.add_argument('satu')
argh.add_argument('dua')
pus = argh.parse_args()

unsur = ['HCl', 'NaOH']
pecah = ['H Cl', 'Na OH']
pecahi = ['H+ Cl-', 'Na+ OH-']
tipe = ['asam', 'basa']


hit = 0
try:
  while not (pus.satu == unsur[hit]):
    hit = hit + 1
  print pus.satu+" adalah "+tipe[hit]
  usatu = hit
except IndexError:
  print "Unsur "+pus.satu+" tidak ditemukan!"
  salah = True
  
hit = 0
try:
  while not (pus.dua == unsur[hit]):
    hit = hit + 1
  print pus.dua+" adalah "+tipe[hit]
  udua = hit
except IndexError:
  print "Unsur "+pus.dua+" tidak ditemukan!"
  salah = True

if salah == True:
  exit()
  

if (tipe[usatu] == 'asam' and tipe[udua] == 'basa'):
  print "Reaksi: Asam dan Basa"
  hasil1 = pecah[usatu].split(" ")
  hasil2 = pecah[udua].split(" ")
  hasil = hasil2[0]+hasil1[1]
  print "Hasil: "+hasil+" + H2O"
if (tipe[usatu] == 'basa' and tipe[udua] == 'asam'):
  print "Reaksi: Asam dan Basa"
  hasil1 = pecah[usatu].split(" ")
  hasil2 = pecah[udua].split(" ")
  hasil = hasil1[0]+hasil2[1]
  print "Hasil: "+hasil+" + H2O"
