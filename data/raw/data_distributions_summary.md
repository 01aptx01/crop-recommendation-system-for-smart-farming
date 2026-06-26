# Data Distributions Summary

จากการตรวจสอบค่าสถิติ (Min-Max และค่าเฉลี่ย) และวาดกราฟการกระจายของข้อมูล (Boxplots) จากทั้ง 9 ไฟล์ พบข้อสังเกตที่สำคัญเกี่ยวกับการนำข้อมูลมารวมกันดังนี้ครับ:

## Boxplot Distributions (การกระจายตัวของข้อมูล)
คุณสามารถเลื่อนดูภาพกราฟด้านล่างนี้ เพื่อเปรียบเทียบการกระจายตัวของแต่ละตัวแปรข้าม Dataset ต่างๆ ได้ครับ (แกน Y คือค่าของตัวแปรนั้นๆ)

````carousel
![Distribution of N](/Users/pathcharapisit/.gemini/antigravity-ide/brain/b2c80063-4f57-4c61-8ec6-789f4cf50b21/n_distribution.png)
<!-- slide -->
![Distribution of P](/Users/pathcharapisit/.gemini/antigravity-ide/brain/b2c80063-4f57-4c61-8ec6-789f4cf50b21/p_distribution.png)
<!-- slide -->
![Distribution of K](/Users/pathcharapisit/.gemini/antigravity-ide/brain/b2c80063-4f57-4c61-8ec6-789f4cf50b21/k_distribution.png)
<!-- slide -->
![Distribution of PH](/Users/pathcharapisit/.gemini/antigravity-ide/brain/b2c80063-4f57-4c61-8ec6-789f4cf50b21/ph_distribution.png)
<!-- slide -->
![Distribution of Temperature](/Users/pathcharapisit/.gemini/antigravity-ide/brain/b2c80063-4f57-4c61-8ec6-789f4cf50b21/temperature_distribution.png)
<!-- slide -->
![Distribution of Rainfall](/Users/pathcharapisit/.gemini/antigravity-ide/brain/b2c80063-4f57-4c61-8ec6-789f4cf50b21/rainfall_distribution.png)
<!-- slide -->
![Distribution of Humidity](/Users/pathcharapisit/.gemini/antigravity-ide/brain/b2c80063-4f57-4c61-8ec6-789f4cf50b21/humidity_distribution.png)
````

> [!WARNING]
> **ข้อสังเกตที่ต้องระวังก่อนการรวมข้อมูล (Merge/Concat):**
> 
> 1. **หน่วยของ Rainfall (ปริมาณน้ำฝน) ต่างกันชัดเจน:** ไฟล์อย่าง `crop-yield.csv`, `crop_yield.csv` และ `Crop and fertilizer dataset.csv` มีค่า Rainfall ระดับ **300 - 5200+** ในขณะที่ `Crop_Recommendation.csv` และ `original_dataset.csv` อยู่ในช่วง **20 - 300** เป็นไปได้ว่าแหล่งแรกเก็บเป็น **มิลลิเมตร/ปี** หรือคนละหน่วยเวลา
> 2. **ค่า K (Potassium) ผิดปกติในบางไฟล์:** `Crop Recommendation using Soil Properties and Weather Prediction.csv` มีค่า K พุ่งไปถึง **2119** (Mean = 324) ซึ่งสูงกว่าไฟล์อื่นๆ (ที่ Max มักจะอยู่แค่ 85 - 200) มากๆ และค่า N ดันเข้าใกล้ศูนย์ (Max = 0.70) ซึ่งแปลว่า Scale ไม่ใช่หน่วยน้ำหนักแบบเดียวกันแน่นอน
> 3. **ค่า Humidity (ความชื้น) ที่ต่างกัน:** ไฟล์ `Crop Recommendation using Soil Properties and Weather Prediction.csv` มีความชื้นเฉลี่ยแค่ **10%** ในขณะที่ไฟล์อื่นเฉลี่ย **60-70%** (อาจจะเป็นคนละหน่วย หรือเป็นการวัดคนละรูปแบบ)
> 4. **ตาราง `data_core.csv` ขาดความสมดุลเรื่อง NPK:** สังเกตจากตารางสรุปด้านล่าง P และ K มักจะมีค่าน้อยมากจนถึง 0 เป็นส่วนใหญ่

---

## ตารางสรุปค่า Min-Max (Summary Tables)

### สารอาหารในดิน (NPK)
| Dataset | N (Min-Max) | P (Min-Max) | K (Min-Max) |
|:---|:---|:---|:---|
| Crop_Recommendation.csv | 0.0 - 140.0 | 5.0 - 145.0 | 5.0 - 205.0 |
| original_dataset.csv | 0.0 - 120.0 | 5.0 - 80.0 | 5.0 - 85.0 |
| data_core.csv | 0.0 - 46.0 | 0.0 - 46.0 | 0.0 - 23.0 |
| crop-yield.csv | 30.0 - 179.0 | 15.0 - 99.0 | 20.0 - 149.0 |
| crop_data.csv | 10.0 - 250.0 | 10.0 - 158.0 | 10.0 - 615.0 |
| crop_yield.csv | 50.0 - 150.0 | 15.0 - 55.0 | 20.0 - 50.0 |
| Crop_recommendation-3.csv | 0.0 - 140.0 | 5.0 - 145.0 | 5.0 - 205.0 |
| Crop and fertilizer dataset.csv | 20.0 - 150.0 | 10.0 - 90.0 | 5.0 - 150.0 |
| Crop Rec (Soil & Weather) | 0.0 - 0.70 | 0.0 - 782.0 | 41.13 - 2119.0 |

### สภาพแวดล้อม (Environment)
| Dataset | PH | Temp (°C) | Rainfall | Humidity (%) |
|:---|:---|:---|:---|:---|
| Crop_Recommendation.csv | 3.5 - 9.94 | 8.83 - 43.68 | 20.21 - 298.56 | 14.26 - 99.98 |
| original_dataset.csv | 5.01 - 8.87 | 10.01 - 34.95 | 20.21 - 298.56 | 14.26 - 95.00 |
| data_core.csv | - | 20.0 - 40.0 | - | 40.02 - 80.0 |
| crop-yield.csv | 4.8 - 8.2 | 10.0 - 40.0 | 300.70 - 2799.26 | 30.01 - 89.99 |
| crop_data.csv | 3.82 - 7.6 | 8.0 - 38.0 | 15.34 - 2817.86 | - |
| crop_yield.csv | 5.5 - 8.0 | 6.26 - 28.63 | 249.24 - 5244.36 | 34.47 - 86.06 |
| Crop and fertilizer dataset.csv | 5.5 - 8.5 | 10.0 - 40.0 | 300.0 - 1700.0 | - |
| Crop Rec (Soil & Weather) | 4.3 - 8.5 | 13.94 - 21.62 | - | 8.60 - 11.71 |
