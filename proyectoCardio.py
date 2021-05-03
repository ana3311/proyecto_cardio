# -*- coding: utf-8 -*-
"""ProyectoCardio.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BO_bnXAKCtUOd1r5V7ONBpkmsjzMTSSo
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sb
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.layers.normalization import BatchNormalization
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
import keras

import warnings

warnings.filterwarnings('ignore')

def load_file():
  data = pd.read_csv("cardioBueno.csv",sep=",")
  return data
  
def modify_atipic_height_values_with_mean(number_of_records, data):
  all_height_values = data["height"]
  
  for row in range(0,number_of_records):
    value_of_height_record = data["height"][row]
    if value_of_height_record <= 130 or value_of_height_record >= 220:
      data["height"][row] = all_height_values.mean()

def modify_atipic_ap_lo_values_with_mean(number_of_records, data):
  all_ap_lo_values = data["ap_lo"]

  for row in range(0,number_of_records):
    value_of_ap_lo_record = data["ap_lo"][row]
    if value_of_ap_lo_record <= 50 or value_of_ap_lo_record >= 170:
      data["ap_lo"][row] = all_ap_lo_values.mean()

def modify_atipic_ap_hi_values_with_mean(number_of_records, data):
  all_ap_hi_values = data["ap_hi"]

  for row in range(0,number_of_records):
    value_of_ap_hi_record = data["ap_hi"][row]
    if value_of_ap_hi_record <= 80 or value_of_ap_hi_record >= 200:
      data["ap_hi"][row] = all_ap_hi_values.mean()

def modify_atipic_weight_values_with_mean(number_of_records, data):
  all_weight_values = data["weight"]

  for row in range(0,number_of_records):
    value_of_weight_record = data["weight"][row]
    if value_of_weight_record <= 50:
      data["weight"][row] = all_weight_values.mean()

def modify_all_atipic_values_with_mean(number_of_records, data):
  modify_atipic_height_values_with_mean(number_of_records, data)
  modify_atipic_ap_lo_values_with_mean(number_of_records, data)
  modify_atipic_ap_hi_values_with_mean(number_of_records, data)
  modify_atipic_weight_values_with_mean(number_of_records, data)

def check_null_values(data):
  print("Tenemos", np.sum(np.sum(data.isna())), "valores Nulos")

def check_if_balanced_targets(data):
  percentage_of_people_with_cardiovascular_disease = np.sum(data['cardio']) * 100 / len(data['cardio'])
  if percentage_of_people_with_cardiovascular_disease >= 45 and percentage_of_people_with_cardiovascular_disease <= 55:
    print("El porcentaje de ataques en personas con enfermedades cardiovasculares es: ", percentage_of_people_with_cardiovascular_disease, "%")
    print("El target está equilibrado")
  else:
    print("El porcentaje de ataques en personas con enfermedades cardiovasculares es: ", percentage_of_people_with_cardiovascular_disease, "%")
    print("El target NO está equilibrado")

#Comprobamos el rango de edades
def plot_age_range(data):
  plt.figure(figsize=(10,5))
  plt.hist(data['age'], color = 'aquamarine', edgecolor='blue', linewidth=0.5, bins=36)
  plt.title('Rango y Número de edades')
  plt.xlabel('Edades (Años)')
  plt.ylabel('Nº de veces en los datos')
  plt.show()

  min_value_age = data['age'].min()
  max_value_age = data['age'].max()

  print("El valor minimo de edad es", min_value_age)
  print("El valor máximo de edad es", max_value_age)

def plot_height_range(data):
  no_outliers = [120, 200]
  plt.hist(data['height'],color = 'aquamarine', 
           edgecolor='blue', linewidth=0.5, bins=50, range=no_outliers)

  plt.title('Rango de alturas')
  plt.xlabel('Alturas (Cm)')
  plt.ylabel('Nº de veces en los datos')
  plt.show()

  min_value_height = data['height'].min()
  max_value_height = data['height'].max()

  print("El valor minimo de altura es", min_value_height)
  print("El valor máximo de altura es", max_value_height)

def plot_weight_range(data):
  no_outliers = [30, 150]
  plt.hist(data['weight'],color = 'aquamarine',edgecolor='blue', 
          linewidth=0.5, bins=50, range=no_outliers)

  plt.title('Rango de pesos')
  plt.xlabel('Pesos (Kg)')
  plt.ylabel('Nº de veces en los datos')
  plt.show()

  min_value_weight = data['weight'].min()
  max_value_weight = data['weight'].max()

  print("El valor minimo del peso es", min_value_weight)
  print("El valor máximo del peso es", max_value_weight)

def data_statistics_per_gender(data, number_of_records):
  all_people_with_cardiovascular_disease = data["cardio"] == 1
  all_woman_records_in_dataset = data['gender'] == 1
  all_man_records_in_dataset = data['gender'] == 2

  people_with_cardiovascular_disease = data[all_people_with_cardiovascular_disease]
  woman_with_cardiovascular_disease = people_with_cardiovascular_disease['gender'] == 1
  man_with_cardiovascular_disease = people_with_cardiovascular_disease['gender']==2

  woman_percentage_in_dataset = np.sum(all_woman_records_in_dataset) / number_of_records*100
  woman_percentage_with_cardiovascular_disease = np.sum(woman_with_cardiovascular_disease)/(number_of_records*woman_percentage_in_dataset/100)*100
  man_percentage_in_dataset = (np.sum(all_man_records_in_dataset)/number_of_records*100)
  man_percentage_with_cardiovascular_disease = np.sum(man_with_cardiovascular_disease)/(number_of_records*man_percentage_in_dataset/100)*100

  print("El porcentaje de mujeres es:", woman_percentage_in_dataset,"%")
  print("de las cuales, un:", woman_percentage_with_cardiovascular_disease, "% han sufrido enfermedades cardiovasculares")
  print("El porcentaje de hombres es:", man_percentage_in_dataset,"%")
  print("de las cuales, un:", man_percentage_with_cardiovascular_disease,"% han sufrido enfermedades cardiovasculares")

def data_statistics_cholesterol(data, number_of_records):
  people_with_cholesterol_normal_value = data['cholesterol']==1
  number_of_people_with_cholesterol_normal_value = len(data[people_with_cholesterol_normal_value])
  normal_cholesterol_percentage = np.round(number_of_people_with_cholesterol_normal_value/number_of_records*100,2)

  people_with_cholesterol_above_normal = data['cholesterol']==2
  number_of_people_with_cholesterol_above_normal_value = len(data[people_with_cholesterol_above_normal])
  above_normal_cholesterol_percentage = np.round(number_of_people_with_cholesterol_above_normal_value/number_of_records*100,2)

  people_with_higth_cholesterol = data['cholesterol']==3
  number_of_people_with_high_cholesterol_value = len(data[people_with_higth_cholesterol])
  high_cholesterol_percentage = np.round(number_of_people_with_high_cholesterol_value/number_of_records*100,2)

  print("El porcentaje de colesterol normal es:", normal_cholesterol_percentage, "%")
  print("El porcentaje de colesterol sobre lo normal es:", above_normal_cholesterol_percentage, "%")
  print("El porcentaje de colesterol muy por encima de lo normal es:", high_cholesterol_percentage, "%")

def data_statistics_glucose(data, number_of_records):
  people_with_glucose_normal_value = data['gluc']==1
  number_of_people_with_glucose_normal_value = len(data[people_with_glucose_normal_value])
  normal_glucose_percentage = np.round(number_of_people_with_glucose_normal_value/number_of_records*100,2)

  people_with_glucose_above_normal = data['gluc']==2
  number_of_people_with_glucose_above_normal_value = len(data[people_with_glucose_above_normal])
  above_normal_glucose_percentage = np.round(number_of_people_with_glucose_above_normal_value/number_of_records*100,2)

  people_with_higth_glucose = data['gluc']==3
  number_of_people_with_high_glucose_value = len(data[people_with_higth_glucose])
  high_glucose_percentage = np.round(number_of_people_with_high_glucose_value/number_of_records*100,2)

  print("El porcentaje de glucosa normal es:", normal_glucose_percentage, "%")
  print("El porcentaje de glucosa sobre lo normal es:", above_normal_glucose_percentage, "%")
  print("El porcentaje de glucosa muy por encima de lo normal es:", high_glucose_percentage, "%")

def data_statistics_smokers(data, number_of_records):
  smokers_people = data['smoke']==1
  number_of_smokers_people = len(data[smokers_people])
  smokers_percentage = np.round(number_of_smokers_people/number_of_records*100,2)

  print("El porcentaje de personas fumadoras es:", smokers_percentage,"%")

def data_statistics_alcohol(data, number_of_records):
  people_who_drink_alcohol = data['alco']==1
  number_of_people_who_drink_alcohol = len(data[people_who_drink_alcohol])
  people_who_drink_alcohol_percentage = np.round(number_of_people_who_drink_alcohol/number_of_records*100,2)

  print("El porcentaje de personas que consumen alcohol es:", people_who_drink_alcohol_percentage, "%")

def data_statistics_active_people(data, number_of_records):
  active_people = data['active'] == 1
  number_of_active_people = len(data[active_people])
  active_people_percentage = np.round(number_of_active_people/number_of_records*100,2)

  print("El porcentaje de personas activas es:", active_people_percentage, "%")

def plot_pressure_cholesterol_relation_people_with_cardiovascular_disease(data):
  normal_cholesterol = data[data["cholesterol"] == 1]
  high_cholesterol = data[data["cholesterol"] == 3]

  people_with_normal_cholesterol_and_cardiovascular_disease = normal_cholesterol[normal_cholesterol["cardio"] == 1]
  people_with_normal_cholesterol_without_cardiovascular_disease = normal_cholesterol[normal_cholesterol["cardio"] == 0]

  people_with_high_cholesterol_and_cardiovascular_disease = high_cholesterol[high_cholesterol["cardio"] == 1]
  people_with_high_cholesterol_without_cardiovascular_disease = high_cholesterol[high_cholesterol["cardio"] == 0]

  plt.scatter(people_with_normal_cholesterol_and_cardiovascular_disease["ap_lo"],
              people_with_normal_cholesterol_and_cardiovascular_disease["ap_hi"],
              color = "aquamarine", edgecolor = "black", label = "Normal con problemas")
  
  plt.scatter(people_with_normal_cholesterol_without_cardiovascular_disease["ap_lo"],
              people_with_normal_cholesterol_without_cardiovascular_disease["ap_hi"],
              color = "red", edgecolor = "black", label = "Normal sin problemas")
  
  plt.scatter(people_with_high_cholesterol_and_cardiovascular_disease["ap_lo"], 
              people_with_high_cholesterol_and_cardiovascular_disease["ap_hi"], 
              color = "green", edgecolor = "black", label = "Alto con problemas")
  
  plt.scatter(people_with_high_cholesterol_without_cardiovascular_disease["ap_lo"],
              people_with_high_cholesterol_without_cardiovascular_disease["ap_hi"],
              color = "yellow", edgecolor = "black", label = "Alto sin problemas")

  plt.title("Relación Presión - colesterol")
  plt.xlabel("Presión diastólica (baja)")
  plt.ylabel("Presión sistólica (alta)")
  plt.legend()
  plt.show()

def plot_pressure_cholesterol_relation(data):
  people_with_normal_cholesterol = data[data["cholesterol"] == 1]
  people_with_high_cholesterol = data[data["cholesterol"] == 3]

  plt.scatter(people_with_normal_cholesterol["ap_lo"], people_with_normal_cholesterol["ap_hi"],
              color = "aquamarine", edgecolor = "black", label = "Colesterol normal")

  plt.scatter(people_with_high_cholesterol["ap_lo"], people_with_high_cholesterol["ap_hi"], 
              color = "red", edgecolor = "black", label = "Colesterol muy alto")

  plt.title("Relación Presión - colesterol")
  plt.xlabel("Presión diastólica (baja)")
  plt.ylabel("Presión sistólica (alta)")
  plt.legend()
  plt.show()

def plot_pressure_active_relation(data):
  active_people = data[data["active"] == 1]
  no_active_people = data[data["active"] == 0]

  plt.scatter(active_people["ap_lo"], active_people["ap_hi"], color = "aquamarine",
              edgecolor = "black", label = "Activos")
  
  plt.scatter(no_active_people["ap_lo"], no_active_people["ap_hi"], color = "red",
              edgecolor = "black", label = "No activos")
  
  plt.title("Relación Presión - actividad física")
  plt.xlabel("Presión diastólica (baja)")
  plt.ylabel("Presión sistólica (alta)")
  plt.legend()
  plt.show()

def plot_pressure_smokers_relation(data):
  smoker = data[data["smoke"] == 1]
  no_smoker = data[data["smoke"] == 0]

  plt.scatter(no_smoker["ap_lo"], no_smoker["ap_hi"], color = "red",
              edgecolor = "black", label = "No fumador")

  plt.scatter(smoker["ap_lo"], smoker["ap_hi"],
              color = "aquamarine", edgecolor = "black", label = "Fumador")

  plt.title("Relación Presión - Fumador / No fumador")
  plt.xlabel("Presión diastólica (baja)")
  plt.ylabel("Presión sistólica (alta)")
  plt.legend()
  plt.show()

def correlation_matrix(data):
  data_without_target = data.drop(['cardio'],axis=1)
  correlation_matrix = data_without_target.corr()
  plt.subplots(figsize=(13,10))
  sb.heatmap(correlation_matrix, cmap='RdBu_r', vmin=-1, vmax=1, square=True, 
             linewidths=.2, annot = True, annot_kws={"size": 7})

def obtain_X_Y_targets(data):
  Y = data['cardio']
  X = data.drop(['cardio'], axis=1)

  scaler = MinMaxScaler()
  scaled_X = scaler.fit_transform(X)
  X = pd.DataFrame(scaled_X)

  return X,Y

def split_train_test_dataset(X, Y):
  X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.3)
  return X_train, X_test, y_train, y_test

def create_model():
  model = Sequential()
  model.add(Dense(32, input_dim=11))
  model.add(BatchNormalization())
  model.add(Activation('relu'))

  model.add(Dense(16))
  model.add(BatchNormalization())
  model.add(Activation('relu'))

  model.add(Dense(8))
  model.add(Activation('relu'))

  model.add(Dense(1,activation='sigmoid'))

  return model
  
def compile_model(model):
  model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

def fit_model(X_train, y_train, X_test,y_test, model):
  callbacks = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)

  acc = model.fit(X_train, y_train, 
                  epochs=15,
                  callbacks=[callbacks],
                  batch_size=32,
                  validation_data=(X_test,y_test))
  
  return acc

def plot_loss_and_val_loss(acc):
  plt.xlabel("Epochs")
  plt.ylabel("Error")
  plt.plot(acc.history["loss"], label = "loss")
  plt.plot(acc.history["val_loss"], label = "val_loss")
  plt.legend()
  plt.show()

def evaluate_model(X_test,y_test, model):
  model.evaluate(X_test,y_test, verbose=0)

def main():
  data = load_file()
  number_of_records = data.count()[0]
  modify_all_atipic_values_with_mean(number_of_records, data)

  check_null_values(data)
  check_if_balanced_targets(data)

  plot_age_range(data)
  plot_height_range(data)
  plot_weight_range(data)

  data_statistics_per_gender(data, number_of_records)
  data_statistics_cholesterol(data, number_of_records)
  data_statistics_glucose(data, number_of_records)
  data_statistics_smokers(data, number_of_records)
  data_statistics_alcohol(data, number_of_records)
  data_statistics_active_people(data, number_of_records)

  plot_pressure_cholesterol_relation_people_with_cardiovascular_disease(data)
  plot_pressure_cholesterol_relation(data)
  plot_pressure_active_relation(data)
  plot_pressure_smokers_relation(data)

  correlation_matrix(data)

  X, Y = obtain_X_Y_targets(data)
  X_train, X_test, y_train, y_test = split_train_test_dataset(X, Y)
  model = create_model()
  compile_model(model)
  acc = fit_model(X_train, y_train, X_test,y_test, model)
  plot_loss_and_val_loss(acc)
  
  evaluate_model(X_test,y_test, model)

main()