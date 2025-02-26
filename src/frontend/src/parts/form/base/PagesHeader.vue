<template>
    <span class="header-container">
        <div class="logo" style="width: 64px; height: 64px"></div>
        <div class="header">
            <div class="flex-container-row">
                <BaseBtn :outline="isSelected('home')" :inactive="!isSelected('home')" @click="toHomePage"> Расписание </BaseBtn>
                <BaseBtn :outline="isSelected('groups')" :inactive="!isSelected('groups')" @click="toMyGroups"> Мои группы </BaseBtn>
                <BaseBtn :outline="isSelected('slots')" :inactive="!isSelected('slots')" :disabled="true" @click="logout"> Мои окна </BaseBtn>
                <BaseBtn :outline="isSelected('logout')" :inactive="!isSelected('logout')" @click="logout"> Выйти </BaseBtn>
            </div>
        </div>
        {{ currentUser?.name }}
        <router-link :to="`/user/show/${currentUser?.id}`">
            <img class="profile-pic" :src="imageSrc" />
        </router-link>
    </span>
</template>
<script>
import { BASE_URL } from '@/api/api.settings'
export default {
    data() {
        return {
            currentUser: null,
            BASE_URL: BASE_URL,
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
        isSelected(page) {
            return this.$route?.fullPath.search(page) === 1
        },
        toHomePage() {
            this.$router.push('/home')
        },
        toMyGroups() {
            this.$router.push(`/groups/list?user_id=${this.currentUser?.id}`)
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
        currentUserId() {
            return this.$ls.current_user ?? null
        },
        imageSrc() {
            return `${this.BASE_URL}/images/default-pic.jpg`
        },
    },
    created() {
        if (this.currentUserId !== null) this.getCurrentUser()
    },
}
</script>
