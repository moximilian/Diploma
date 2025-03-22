<template>
    <TableView
        ref="table"
        :keys="keys"
        displayName="participants"
        :defaultFilters="defaultFilters"
        :filters="defaultFilters"
        :isClickable="false"
    >
        <template #first-item="{ row }">
            <TableCellCheckBox
                v-if="canEdit"
                @clickCheckBox="isChecked => onCheckboxChecked(isChecked, row)"
            />
        </template>
        <template #after-table="{ rows }">
            <BaseBtn
                v-if="canEdit && rows.length > 0"
                value="Исключить"
                @click="removeParticipans"
            />
        </template>
    </TableView>
</template>

<script>
export default {
    props: {
        groupId: { type: String, default: () => '' },
        entity: { type: Object, default: () => {} },
    },
    data() {
        return {
            keys: [
                {
                    name: 'fio',
                    title: 'ФИО участника',
                    format: row => [row.name, row.surname, row.last_name].join(' '),
                },
                { name: 'login' },
            ],
            selectedIds: new Map(),
        }
    },
    methods: {
        onCheckboxChecked(isChecked, { id }) {
            isChecked ? this.selectedIds.set(id, true) : this.selectedIds.delete(id, true)
        },
        removeParticipans() {
            this.$api.participants.delete(
                { ids: Array.from(this.selectedIds).map(item => item[0]) },
                () => {
                    this.$refs.table.load()
                }
            )
        },
    },
    computed: {
        canEdit() {
            return this.$ls.current_user == this.entity?.creator_id ?? false
        },
        defaultFilters() {
            return {
                filters: {
                    wheres: [
                        {
                            column: 'group_id',
                            value: this.groupId,
                        },
                    ],
                },
            }
        },
    },
}
</script>
