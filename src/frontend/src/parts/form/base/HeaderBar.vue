<template>
    <span>
        <span class="header-container">
            <div class="header">
                <BaseBtn v-if="!isAuthorized" @click="toRegisterPage"> Sign Up </BaseBtn>
                <div v-else class="flex-container-row">
                    <router-link :to="`/user/show/${currentUser?.id}`">{{ currentUser?.name }}</router-link>
                    <BaseBtn @click="toHomePage"> Home </BaseBtn>
                    <BaseBtn @click="logout" :disabled="!isAuthorized"> Log Out </BaseBtn>
                </div>
            </div>
        </span>
    </span>
</template>
<script>
export default {
    data() {
        return {
            currentUser: null,
        }
    },
    watch: {
        currentUserId() {
            this.currentUserId && this.getCurrentUser()
        },
    },
    methods: {
        toRegisterPage() {
            this.$router.push('/auth/login')
        },
        toHomePage() {
            this.$router.push('/home')
        },
        logout() {
            this.$api.auth.logout({ access_token: this.$ls.token }, () => {
                this.$ls.token = null
                this.$ls.current_user = null
                this.$router.push('/auth/login')
            })
        },
        getCurrentUser() {
            this.$api.users.one({ id: this.$ls.current_user }, res => {
                this.currentUser = res
            }) ?? ''
        },
    },
    computed: {
        isForm() {
            return this.$route.path.includes('auth')
        },
        accessToken() {
            return this.$ls.token
        },
        isAuthorized() {
            return !!this.accessToken // && getUser()
        },
        currentUserId() {
            return this.$ls.current_user ?? null
        },
    },
    created() {
        if (this.currentUserId !== null) this.getCurrentUser()
    },
}
</script>
