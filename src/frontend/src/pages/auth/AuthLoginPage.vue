<template>
    <div>
        <h1>Login Page</h1>
        <p>Please log in to access more features.</p>
        <div>
            <p>Not have an account yet?</p>
            <router-link to="/auth/register">Register</router-link>
        </div>
        <router-link to="/home">Go Back to Home</router-link>
    </div>
    <FormBase displayName="login" :onlyEdit="true">
        <template #form-bottom="{entity}">
            <BaseBtn @click="authorize(entity)">Log In</BaseBtn>
        </template>
    </FormBase>
</template>

<script>
export default {
    methods: {
        authorize(entity) {
            this.$api.auth.login({...entity}, res => {
                if (res.detail) return
                this.$ls.token = res.access_token
                this.$ls.current_user = res.user_id
                this.$router.replace('/home')
            })
        },
    },
}
</script>