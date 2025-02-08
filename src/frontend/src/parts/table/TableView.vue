<template>
    <TableBase 
        :keys="keys"
        :rows="rows"
    >
        <template #before>
            <slot name="before"></slot>
        </template>
    </TableBase>
</template>
<script>
import TableBase  from './TableBase.vue'
export default {
    props: {
        displayName: { type: String, default: () => null },
        keys: { type: Array, default: () => [] },
        defaultFilters:{ type: Object, default: () => {} }, 
    },
    data() {
        return {
            rows: [],
            totalCount: 0,
        }
    },
    created() {
        if (!this.displayName) {
            return console.error('TableView: display rule is not provided')
        }
        this.$api[this.displayName].list(this.defaultFilters, (res) => {
            if (res.detail) return console.error('Error during API call')
            this.rows = res.rows
            this.totalCount = res.totalCount
        })
    },
    components: {TableBase},
}
</script>
