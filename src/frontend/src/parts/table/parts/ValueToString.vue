<template>
    {{ viewValue }}
</template>
<script>
export default {
    props: {
        row: { type: Object, default: () => {} },
        keyName: { type: String, default: () => '' },
        field: { type: Object, default: () => {} },
    },
    data() {
        return {
            realValue: '',
        }
    },
    computed: {
        viewValue() {
            if (this.realValue.length > 64) {
                const toDelete = this.realValue.substring(64, this.realValue.length)
                return this.realValue.replace(toDelete, '') + '...'
            }
            return this.realValue
        },
    },

    async created() {
        const { body, ok } = await this.$api[this.field.displayName].one({
            [this.field.fieldKey ?? 'id']: this.row[this.field.localKeyName],
        })
        if (!ok) return
        this.realValue = Array.isArray(this.field.showName)
            ? this.field.showName.map(field => body[field]).join(' ')
            : body[this.field.showName]
    },
}
</script>
