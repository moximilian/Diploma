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
    <div class="form">
        <input name="login" type="text" required v-model="loginValue" />
        <input name="password" type="password" required v-model="passwordValue" />

        <BaseBtn @click="authorize">Log In</BaseBtn>
    </div>
</template>

<script>
export default {
    data() {
        return {
            loginValue: '',
            passwordValue: '',

        }
    },
    methods: {
        authorize() {
            this.$api.auth.login({ login: this.loginValue, password: this.passwordValue }, res => {
                this.$ls.token = res.access_token
                this.$ls.current_user = res.user_id
                console.log(res)
                this.$router.replace('/home')
            })
        },


    },
    created() {
        console.log('token', this.$ls.token)
    },
}
</script>
<style>
.form {
    display: flex;
    flex-direction: column;
    gap: 15px;
    align-items: center;
}
</style>
