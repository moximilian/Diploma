<template>
    <div class="auth-form">
        <div class="page-title">Вход</div>
        <FormView displayName="login" action="edit">
            <template #form-bottom="{ entity }">
                <BaseBtn @click="authorize(entity)">Войти</BaseBtn>
            </template>
        </FormView>
    </div>
</template>

<script>
export default {
    methods: {
        authorize(entity) {
            this.$api.auth.login({ ...entity }, res => {
                if (res?.detail) return
                this.$ls.token = res.access_token
                this.$ls.current_user = res.user_id
                this.$store.commit('setUser', res.user_id)
                this.$router.replace('/home')
            })
        },
    },
}
</script>
