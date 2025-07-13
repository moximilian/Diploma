<template>
    <span>
        <AuthPagesHeader v-if="!isAuthorized" />
        <PagesHeader v-else />
    </span>
</template>
<script>
import AuthPagesHeader from '../../../pages/auth/_help/AuthPagesHeader.vue'
import PagesHeader from './PagesHeader.vue'
export default {
    computed: {
        accessToken() {
            return this.$ls.token
        },
        isAuthorized() {
            return !!this.accessToken // && getUser()
        },
    },
    components: { AuthPagesHeader, PagesHeader },
}
</script>
