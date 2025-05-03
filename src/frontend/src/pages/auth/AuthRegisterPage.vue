<template>
    <div class="auth-form">
        <div class="page-title">Регистрация</div>
        <FormView displayName="register" action="edit" @onSave="register">
            <template #form-bottom="{ entity }">
                <BaseBtn @click="register(entity)">Зарегистрироваться</BaseBtn>
            </template>
        </FormView>
        <span>*Нажимая кнопку, соглашаюсь с <a href="">условиями обработки данных</a></span>
    </div>
</template>

<script>
export default {
    methods: {
        async register(entity) {
            await this.$api.auth.register(entity)
            this.$router.push('/auth/login')
        },
    },
    mounted() {
        if (![null, '', undefined].includes(this.$ls.token)) {
            this.$router.replace('/home')
        }
    }
}
</script>
