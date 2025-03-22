<template>
    <TableBase :keys="keys" :rows="rows" :displayName="displayName" :isClickable="isClickable">
        <template #before>
            <slot name="before"></slot>
        </template>
        <template #first-item="{ row }">
            <slot name="first-item" :row="row"></slot>
        </template>
        <template #last-item="{ row }">
            <slot name="last-item" :row="row"></slot>
        </template>
    </TableBase>
    <div class="after-table-continer">
        <div class="after-table">
            <slot name="after-table" :rows="rows"></slot>
        </div>
    </div>
</template>
<script>
import TableBase from './TableBase.vue'
export default {
    props: {
        displayName: { type: String, default: () => null },
        keys: { type: Array, default: () => [] },
        defaultFilters: { type: Object, default: () => {} },
        filters: { type: Object, default: () => {} },
        isClickable: { type: Boolean, default: () => true },
    },
    data() {
        return {
            rows: [],
            totalCount: 0,
        }
    },
    methods: {
        load() {
            this.rows = []
            this.$api[this.displayName].list({ filters: this.filters }, res => {
                if (res.detail) return console.error('Error during API call')
                this.rows = res.rows
                this.totalCount = res.totalCount
            })
        },
    },
    created() {
        if (!this.displayName) {
            return console.error('TableView: display rule is not provided')
        }
        this.$api[this.displayName].list(this.defaultFilters, res => {
            if (res.detail) return console.error('Error during API call')
            this.rows = res.rows
            this.totalCount = res.totalCount
        })
    },
    components: { TableBase },
}
</script>
