<template>
    <TableBase
        :keys="keys"
        :rows="rows"
        :displayName="displayName"
        :isClickable="isClickable"
        @onCustomKeyDelete="(val, rows) => $emit('onCustomKeyDelete', val, rows)"
        @clickRow="clickRow"
    >
        <template #before>
            <slot name="before"></slot>
        </template>
        <template #custom-title-key="{ rows }">
            <slot name="custom-title-key" :rows="rows"></slot>
        </template>
        <template #first-item="{ row }">
            <slot name="first-item" :row="row"></slot>
        </template>
        <template #last-item="{ row }">
            <slot name="last-item" :row="row"></slot>
        </template>
        <template #table-cell="{ row, keyObj, field }">
            <slot name="table-cell" :row="row" :keyObj="keyObj" :field="field"></slot>
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
        orderByLocal: { type: String, default: () => '' },

        clickRowPath: { type: String, default: () => '' },
    },
    emits: ['loaded', 'onCustomKeyDelete'],
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
                this.defaultSort()
                this.totalCount = res.totalCount
                this.$emit('loaded', this.rows)
            })
        },
        defaultSort() {
            if (!this.orderByLocal) return
            this.rows.sort((first, second) =>
                first[this.orderByLocal] > second[this.orderByLocal] ? 1 : -1
            )
        },
        clickRow(row) {
            const fullPath = this.$route.path
            const source = fullPath.split('/')[1]
            this.$router.push(`/${this.clickRowPath || source}/show/${row.id}`)
        }
    },
    created() {
        if (!this.displayName) {
            return console.error('TableView: display rule is not provided')
        }
        this.$api[this.displayName].list(this.defaultFilters, res => {
            if (res.detail) return console.error('Error during API call')
            this.rows = res.rows
            this.defaultSort()
            this.totalCount = res.totalCount
            this.$emit('loaded', this.rows)
        })
    },
    components: { TableBase },
}
</script>
