<template>
    <div class="auth-header-container">
        <router-link
            v-for="option in options"
            :key="option.name"
            :to="`/auth/${option.name}`"
            class="header-item"
            :class="{ selected: isSelected(option.name) }"
        >
            {{ option.title }}
        </router-link>
    </div>
</template>
<script>
export default {
    data() {
        return {
            options: [
                { name: 'login', title: 'Вход' },
                { name: 'register', title: 'Регистрация' },
            ],
        }
    },
    methods: {
        isSelected(state) {
            return this.$route?.params.action === state
        },
    },
}
</script>
