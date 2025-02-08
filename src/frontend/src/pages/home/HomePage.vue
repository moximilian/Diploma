<template>
    <div class="flex-container-column">
        <BaseBtn @click="getItems" :disabled="!isAuthorized">Test Items request after login</BaseBtn>
        {{ items }}
    </div>
</template>

<script>
export default {
    data() {
        return {
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
        getItems() {
            this.$api.items.list({
                filters: {
                    limit: 0,
                    page: 1,
                },
            }, (res) => {this.items = res})
        },
    }
}
</script>
