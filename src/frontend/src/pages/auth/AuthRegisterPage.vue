<template>
    <div class="auth-form">
        <div class="page-title">Вход</div>
        <FormView displayName="register" action="edit" @onSave="register">
            <template #form-bottom="{ entity }">
                <BaseBtn @click="register(entity)">Зарегистрироваться</BaseBtn>
                <span>*Нажимая кнопку, соглашаюсь с <a href="">условиями обработки данных</a></span>
            </template>
        </FormView>
    </div>
</template>

<script>
export default {
    methods: {
        register(entity) {
            this.$api.auth.register(entity, () => this.$router.push('/auth/login'))
        },
    },
}
</script>
