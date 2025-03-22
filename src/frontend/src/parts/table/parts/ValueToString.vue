<template>
    {{ realValue }}
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

    created() {
        this.$api[this.field.displayName].one(
            { [this.field.fieldKey ?? 'id']: this.row[this.field.localKeyName] },
            res => {
                if (res.detail) return
                this.realValue = Array.isArray(this.field.showName)
                    ? this.field.showName.map(field => res[field]).join(' ')
                    : res[this.field.showName]
            }
        )
    },
}
</script>
