<template>
<div class="repair__wrapper">
    <div class="repair__title">
        <h2>
            <span class="orange">
                Проводится
                техническое обслуживание
            </span>
        </h2>
        <h3>
            Попробуйте зайти
            немного позже
        </h3>
    </div>
    <div class="repair__img__wrapper">
        <img class="repair__img"
             src="./cat502.jpg">
        <span class="repair__img__mark">
            *изображение сгенерировано сервисом
            <span class="orange">chatGPT</span> внутри корпоративного портала</span>
    </div>
</div>
</template>

<style lang="scss">
html {
    background-color: rgba(255, 218, 185, 0.307);
}

.repair__wrapper {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: rgba(255, 218, 185, 0.307);
}

.repair__title {
    margin-top: 20px;
    text-align: center;
    font-family: sans-serif;
    font-size: large;
    font-weight: 600;
    color: #0000009e;
}

.repair__img {
    border-radius: 8px;
    height: 101%;
    width: 620px;
    max-width: 100%;
}

.repair__img__wrapper {
    /* padding: 50px; */
    border: 1px solid rgb(209, 209, 209);
    border-radius: 8px;
    object-fit: cover;
    max-height: 650px;
    /* background: white; */
}

.repair__img__mark {
    display: block;
    text-align: left;
    margin-top: 2px;
    font-size: small;
    font-family: sans-serif;
    font-weight: bold;
    color: #0000009e;
}

.orange {
    color: #ea862f;
}
</style>