<template>
    <div class="mt20">
        <h2 class="page__title">Обратная связь: Есть идея!</h2>
        <p>Добро пожаловать на страницу обратной связи нашего внутрикорпоративного сайта
            Интранет!</p>
        <p>Здесь вы можете поделиться своими идеями и предложениями по улучшению работы компании.</p>
        <p>Ваши идеи могут быть связаны с улучшением бизнес-процессов в компании, с производством, качеством, созданием
            новой техники, повышением квалификации, оптимизации работы в отдельном подразделении или
            внутрикорпоративными событиями.</p>
        <p>Мы всегда открыты к новым идеям и готовы выслушать каждого сотрудника. Давайте работать вместе и делать нашу
            компанию еще лучше!</p>
        <form class="col-sm-6 needs-validation"
              id="feedback-form">
            <input type="hidden"
                   name="section-id"
                   value="319">
            <div class="form-floating mb-3">
                <input type="text"
                       class="form-control"
                       name="form-subject"
                       id="form-subject">
                <label for="form-subject">Тема</label>
                <div class="invalid-feedback">
                    Обязательно укажите тему сообщения
                </div>
            </div>
            <div class="form-floating mb-3">
                <textarea class="form-control"
                          placeholder="Добавьте сообщение"
                          name="form-message"
                          id="form-message"
                          style="height: 200px"></textarea>
                <label for="form-message">Сообщение</label>
                <div class="invalid-feedback">
                    Это поле обязательно для заполнения
                </div>
            </div>
            <div class="mb-3">
                <label for="formFile"
                       class="form-label">Добавить файл</label>
                <input class="form-control"
                       name="attachments-files"
                       type="file"
                       id="formFile">
            </div>
            <div class="mb-3">
                <button type="submit"
                        id="form-submit"
                        class="btn btn-primary">
                    <span class="spinner-border spinner-border-sm"
                          style="display: none"
                          role="status"
                          aria-hidden="true"></span>
                    Отправить
                </button>
            </div>
        </form>

        <div id="thanks"
             class=""
             style="display: none">
            <p>Благодарим Вас за отправку формы обратной связи! Мы обязательно рассмотрим Ваше сообщение и постараемся
                ответить на него как можно скорее. Если у Вас есть какие-либо дополнительные вопросы или пожелания, не
                стесняйтесь обращаться к нам в любое время.</p>
        </div>

        <div id="error"
             class=""
             style="display: none">
            <p>Ошибка! Что-то пошло не так. Сообщите о проблеме разработчику на Email: matrenin.d.e@emk.ru</p>
        </div>

    </div>
</template>

<style>
.form-floating>.form-control:focus,
.form-floating>.form-control:not(:placeholder-shown) {
    padding-top: 1.625rem;
    padding-bottom: .625rem;
}
</style>