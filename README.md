<div align="center">
  <font size=55>
    <h1>
    ARIES
    </h1>
  </font>
</div>

ARIES: Relation Assessment and Model Recommendations for Time Series Forecasting
Submit an article to TPAMI.
Under review

## The repository is currently under construction.

Our baselines come from BasicTS: https://github.com/GestaltCogTeam/BasicTS



___



# 🔮 ARIES: Relation Assessment \& Model Recommendations for Time Series Forecasting



## 📌 Topic  

Recent advancements in deep learning models for \*\*time series forecasting\*\* have been significant.  

These models leverage key properties like **seasonality** ⏳ and **non-stationarity** 📈 as their motivations, indicating a strong link between **model performance** and **data properties**.  





---



## ⚡ Challenges  

- 📉 Benchmark datasets fail to represent **stable and comprehensive temporal patterns**.  

- 🔍 Lack of systematic analysis of the **relationship between data properties and modeling strategies**.  

- ⏱️ No effective **model recommendation system** exists, leading to **time-consuming** and **costly** experimentation.  





---



## 🚀 Our Approach (ARIES)  

We introduce **ARIES**, a unified framework for **assessing the relationship** between time series properties and modeling strategies, and for **recommending deep forecasting models**.  



1. 🧪 **Synthetic Dataset Construction**  

 - Build datasets with **multiple distinct temporal patterns**.  

2. 📊 **Property Computation**  

  - Develop a **comprehensive system** to quantify key time series properties.  

3. 🔬 **Benchmarking 50+ Models**  

  - Establish connections between **data properties** and **forecasting strategies**.  

4. 🤖 **Model Recommendation**  

  - Propose the **first deep forecasting model recommender**, offering **interpretable suggestions** for real-world time series. 

---

## 🤖 Baselines

- **Traditional local forecasting methods:**  
  AR, MA, ARMA, ARIMA, ARCH, GARCH, SARIMA, SES, ETS  

- **Machine learning methods:**  
  SVR, PolySVR, CatBoost, LightGBM  

- **Transformer-based deep learning methods:**  
  Autoformer, Crossformer, DSFormer, ETSformer, FEDformer, Fredformer, Informer, iTransformer, NSformer, PatchTST, Pyraformer, Triformer  

- **MLP-based deep learning methods:**  
  CATS, CycleNet, DLinear, FiLM, FreTS, Koopa, LightTS, MTSMixer, NBeats, NHiTS, NLinear, SOFTS, SparseTSF, STID, TiDE, TimeMixer, TimesNet, UMixer  

- **Foundational models:**  
  MOIRAI (Base & Large), Time-MoE  

- **Others:**  
  DeepAR, HI, SegRNN, Sumba, WaveNet  
