<template>
    <TableView
        ref="table"
        :keys="keys"
        displayName="participants"
        :defaultFilters="defaultFilters"
        :filters="filters"
        :isClickable="false"
    >
        <template #first-item="{ row }">
            <TableCellCheckBox
                v-if="isGroupAdmin"
                @clickCheckBox="isChecked => onCheckboxChecked(isChecked, row)"
            />
        </template>
        <template #after-table="{ rows }">
            <BaseBtn
                v-if="isGroupAdmin && rows?.length > 0"
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
        keys() {
            return [
                ...(this.isGroupAdmin ? [{ name: 'slot', title: 'Выбрать' }] : []),
                {
                    name: 'fio',
                    title: 'ФИО участника',
                    format: row => [row.name, row.surname, row.last_name].join(' '),
                },
                { name: 'login' },
            ]
        },
        isGroupAdmin() {
            return this.$ls.current_user == this.entity?.creator_id ?? false
        },
        filters() {
            return {
                wheres: [
                    {
                        column: 'group_id',
                        value: this.groupId,
                    },
                ],
            }
        },
        defaultFilters() {
            return {
                filters: this.filters,
            }
        },
    },
}
</script>
