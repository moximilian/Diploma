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
    <div class="form">
        <span v-for="field, index of fields" :key="index" class="field">
            <label :for="field.name">{{field.name}}</label> 
            <input :name="field.name" :type="field.type" :required="field.required" v-model="formData[field.name]"
            />
        </span>
        <BaseBtn @click="register">Register</BaseBtn>
    </div>
</template>

<script>
export default {
    data() {
        return {
            loginValue: 'Test',
            passwordValue: 'Testpassworfd1!',
            fields: [
                {
                    name: 'name', value: '', required: true, type:'text'
                },
                {
                    name: 'surname', value: '', required: true, type:'text'
                },
                {
                    name: 'login', value: '', required: true, type:'text'
                },
                {
                    name: 'password', value: '', required: true, type:'text'
                },
                {
                    name: 'password_confirm', value: '', required: true, type:'text'
                },
            ],
            formData: {}
        }
    },
    computed: {
    },
    methods: {
        register() {
            this.$api.auth.register(this.formData, () => this.$router.push('/auth/login'))
        },
    },
    mounted() {
      console.log(this.$api)
    }
}
</script>
<style>
.form {
    display: flex;
    flex-direction: column;
    gap: 15px;
    align-items: center;
}
.field {
    display: flex;
    flex-direction: column;
    gap: 5px;
    align-items: flex-start;
}
</style>
