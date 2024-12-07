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
        <BaseBtn @click="getItems" :disabled="!isAuthorized">Test Items request after login</BaseBtn>
        {{ items }}
    </div>
</template>

<script>
export default {
    data() {
        return {
            loginValue: '',
            passwordValue: '',
            items: {},

        }
    },
    computed: {
        accessToken() {
            return this.$ls.token
        },
        isAuthorized() {
            return !!(this.accessToken) // && getUser()
        },
    },
    methods: {
        authorize() {
            this.$api.auth.login({ login: this.loginValue, password: this.passwordValue }, res => {
                this.$ls.token = res.access_token
                this.$ls.current_user = res.user_id
                console.log(res)
            })
        },
        getItems() {
            this.$api.items.list({
                filters: {
                    limit: 0,
                    page: 1,
                },
            }, (res) => {this.items = res})
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
