<template>
    <div class="table-base-container">
        <slot name="before"> </slot>
        <div class="table-base-body">
            <div class="table-base-header table-base-row">
                <div v-for="key of keys" :key="key" class="table-cell">
                    {{ key.name }}
                </div>
            </div>
            <TableRow v-for="row in rows" :key="row.id" :row="row">
                <div v-for="key of keys" :key="key.name" class="table-cell">
                    {{ row[key.name] }}
                </div>
            </TableRow>
        </div>
    </div>
</template>
<script>
import TableRow from './parts/TableRow.vue';
export default {
    props: {
        keys: { type: Array, default: () => [] },
        rows: { type: Array, default: () => [] },
    },
    components: {
        TableRow
    }
}
</script>
