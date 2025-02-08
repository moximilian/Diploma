<template>
    <div class="table-base-row" @click="changeAction">
        <slot></slot>
    </div>
</template>
<script>
export default {
    props: {
        row: {type: Object, default: () => {}}
    },
    methods: {
        changeAction() {
            const fullPath = this.$route.path
            const source = fullPath.split('/')[1]
            this.$router.push(`/${source}/show/${this.row.id}`)
        }
    }
}
</script>