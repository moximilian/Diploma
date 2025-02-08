<template>
    <div>
        <h1>Register Page</h1>
        <p>Please register in to access more features.</p>
        <div>
            <p>Have an account?</p>
            <router-link to="/auth/login">Login</router-link>
        </div>
        <router-link to="/home">Go Back to Home</router-link>
    </div>
    <FormBase
        displayName="register"
        :onlyEdit="true"
        @onSave="register"
    />
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