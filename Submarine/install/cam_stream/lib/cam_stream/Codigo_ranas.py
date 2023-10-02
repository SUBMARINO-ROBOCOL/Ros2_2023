import cv2
import numpy as np
import matplotlib.pyplot as plt


def conteo_ranas(img, contador, largest_contour, trackers):

    # Etapa de filtrado

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 5)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 111, 6)

    (contours, hierarchy) = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    contours = sorted_contours[1:]


    if len(contours) > 0:
      area = cv2.contourArea(contours[0])
      avg_area = np.mean(area)
      filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 0.3 * avg_area]

      # Halla contorno más grande
      for contour in filtered_contours:
        if largest_contour is None or cv2.contourArea(contour) > cv2.contourArea(largest_contour):
            largest_contour = contour

      #Filtra ruido por tamaño
      filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 0.3 * cv2.contourArea(largest_contour)]

      cv2.drawContours(img, filtered_contours, -1, (0,0,255), 3)


      #Seguimiento de objetos
      if len(trackers) > 0:

          new_trackers = []
          for cnt in filtered_contours:
              x, y, w, h = cv2.boundingRect(cnt)
              previous = False

              for i in range(len(trackers)):
                  tracker, lost_count, active = trackers[i]
                  x2, y2, w2, h2 = tracker

                  if x < x2 + w2 and x + w > x2 and y < y2 + h2 and y + h > y2:
                      previous = True
                      active = True
                      new_trackers.append([[x, y, w, h], 0, active])

              if previous == False:
                  center_x = x + w // 2
                  center_y = y + h // 2
                  w *= 4
                  h *= 4
                  x = center_x - w // 2
                  y = center_y - h // 2
                  height, width, c = img.shape
                  if y < height*0.15:
                      new_trackers.append([[x, y, w, h], 0, False])
                      contador = contador + 1

          for tracker, lost_count, active in trackers:
              if not active:
                  lost_count += 1
                  if lost_count < 20:
                      new_trackers.append([tracker, lost_count, False])

          trackers = new_trackers.copy()

      else:
          # Caso inicial para agregar trackers si la lista está vacía
          for cnt in filtered_contours:
              x, y, w, h = cv2.boundingRect(cnt)
              center_x = x + w // 2
              center_y = y + h // 2
              w *= 4
              h *= 4
              x = center_x - w // 2
              y = center_y - h // 2
              trackers.append([[x, y, w, h], 0, False])
              contador = contador + 1


      return img, contador, largest_contour, trackers
    
def main(img):
    contador = 0
    largest_contour = None
    trackers = []
    
    resp = conteo_ranas(img, contador, largest_contour, trackers)
 
    if resp != None:
        
        processed_frame, contador, largest_contour, trackers = resp
        cv2.putText(processed_frame, "Frogs: " + str(contador), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)
        cv2.imshow("Frog Counting",processed_frame)
        cv2.waitKey(1)
