<script setup>
import { FilterMatchMode } from '@primevue/core/api';
import { useToast } from 'primevue/usetoast';
import { onMounted, ref } from 'vue';
import api from '@/axios';

onMounted(() => {
    api.get('/operations/').then((response) => (operations.value = response.data))
    api.get('/accounts/').then((response) => (dropdownAccounts.value = response.data))
});

const toast = useToast();
const dt = ref();
const operations = ref();
const operationDialog = ref(false);
const deleteOperationDialog = ref(false);
const deleteoperationsDialog = ref(false);
const dropdownAccounts = ref([]);
const dropdownTypes = ref([
    'debit',
    'credit',
    'refund',
    'transfer',
]);
const operation = ref({});
const selectedoperations = ref();
const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS }
});
const submitted = ref(false);

function openNew() {
    operation.value = {};
    submitted.value = false;
    operationDialog.value = true;
}

function hideDialog() {
    operationDialog.value = false;
    submitted.value = false;
}

function saveoperation() {
    operation.value.date = (operation.value.date instanceof Date)
    ? operation.value.date.toISOString().split('T')[0]
    : new Date(operation.value.date).toISOString().split('T')[0];
    submitted.value = true;
    if (operation.value.id) {
        const index = findIndexById(operation.value.id);
        operations.value[index] = { ...operations.value[index], ...operation.value };
        api.put(`/operations/${operation.value.id}/`, operation.value)
            .then(() => {
                operations.value[index] = operation.value;
                operationDialog.value = false;
                operation.value = {};
                toast.add({ severity: 'success', summary: 'Successful', detail: 'OperationUpdated', life: 3000 });
            })
            .catch((error) => {
                console.error(error);
                toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to update operation', life: 3000 });
            });
    } else
    {
    if (operation.value.date && operation.value.destination_account && operation.value.amount) { // Add validation for required fields
        api.post('/operations/', operation.value)
            .then((response) => {
                operations.value.push(response.data); // Add the newly created operation to the list
                operationDialog.value = false;
                operation.value = {};
                toast.add({ severity: 'success', summary: 'Successful', detail: 'OperationCreated', life: 3000 });
            })
            .catch((error) => {
                console.error(error);
                toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to create operation', life: 3000 });
            });
    }
    }
}

function editOperation(prod) {
    operation.value = { ...prod };
    operationDialog.value = true;
}

function confirmDeleteOperation(prod) {
    operation.value = prod;
    deleteOperationDialog.value = true;
}

function deleteoperation() {
    api.delete(`/operations/${operation.value.id}/`)
        .then(() => {
            operations.value = operations.value.filter((val) => val.id !== operation.value.id);
            deleteOperationDialog.value = false;
            operation.value = {};
            toast.add({ severity: 'success', summary: 'Successful', detail: 'OperationDeleted', life: 3000 });
        })
        .catch((error) => {
            console.error(error);
            toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to delete operation', life: 3000 });
        });
}

function findIndexById(id) {
    let index = -1;
    for (let i = 0; i < operations.value.length; i++) {
        if (operations.value[i].id === id) {
            index = i;
            break;
        }
    }

    return index;
}

function exportCSV() {
    dt.value.exportCSV();
}

function confirmDeleteSelected() {
    deleteoperationsDialog.value = true;
}

function deleteSelectedoperations() {
    operations.value = operations.value.filter((val) => !selectedoperations.value.includes(val));
    deleteoperationsDialog.value = false;
    selectedoperations.value = null;
    toast.add({ severity: 'success', summary: 'Successful', detail: 'operations Deleted', life: 3000 });
}
</script>

<template>
    <div>
        <div class="card">
            <Toolbar class="mb-6">
                <template #start>
                    <Button label="New" icon="pi pi-plus" severity="secondary" class="mr-2" @click="openNew" />
                    <Button label="Delete" icon="pi pi-trash" severity="secondary" @click="confirmDeleteSelected" :disabled="!selectedoperations || !selectedoperations.length" />
                </template>

                <template #end>
                    <Button label="Export" icon="pi pi-upload" severity="secondary" @click="exportCSV($event)" />
                </template>
            </Toolbar>

            <DataTable
                ref="dt"
                v-model:selection="selectedoperations"
                :value="operations"
                dataKey="id"
                :paginator="true"
                :rows="10"
                :filters="filters"
                paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                :rowsPerPageOptions="[5, 10, 25]"
                currentPageReportTemplate="Showing {first} to {last} of {totalRecords} operations"
            >
                <template #header>
                    <div class="flex flex-wrap gap-2 items-center justify-between">
                        <h4 class="m-0">Manage operations</h4>
                        <IconField>
                            <InputIcon>
                                <i class="pi pi-search" />
                            </InputIcon>
                            <InputText v-model="filters['global'].value" placeholder="Search..." />
                        </IconField>
                    </div>
                </template>

                <Column selectionMode="multiple" style="width: 3rem" :exportable="false"></Column>
                <Column field="id" header="Id" sortable style="min-width: 12rem"></Column>
                <Column field="date" header="Date" sortable style="min-width: 16rem"></Column>
                <Column field="type" header="Type" sortable style="min-width: 16rem"></Column>
                <Column field="source_account.name" header="Source Account" sortable style="min-width: 16rem"></Column>
                <Column field="destination_account.name" header="Destination Account" sortable style="min-width: 16rem"></Column>
                <Column field="amount" header="Amount" sortable style="min-width: 16rem"></Column>
                <Column field="description" header="Description" sortable style="min-width: 16rem"></Column>
                <Column :exportable="false" style="min-width: 12rem">
                    <template #body="slotProps">
                        <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editOperation(slotProps.data)" />
                        <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeleteOperation(slotProps.data)" />
                    </template>
                </Column>
            </DataTable>
        </div>

        <Dialog v-model:visible="operationDialog" :style="{ width: '450px' }" header="operation Details" :modal="true">
            <div class="flex flex-col gap-6">
                <img v-if="operation.image" :src="`https://primefaces.org/cdn/primevue/images/operation/${operation.image}`" :alt="operation.image" class="block m-auto pb-4" />
                <div>
                    <label for="type" class="block font-bold mb-3">Type</label>
                    <Select v-model="operation.type" :options="dropdownTypes" placeholder="Select a type" :filter="true" :showClear="true">
                        <template #option="slotProps">
                            {{ slotProps.option }}
                        </template>
                        <template #value="slotProps">
                            {{ slotProps.value }}
                        </template>
                    </Select>
                </div>
                <div>
                    <label for="date" class="block font-bold mb-3">Date</label>
                    <DatePicker
                        id="date"
                        v-model="operation.date"
                        :showIcon="true"
                        :placeholder="'Select a date'"
                        :required="true"
                        :invalid="submitted && !operation.date"
                        :showButtonBar="true"
                    />
                </div>
                <div>
                    <label for="source_account" class="block font-bold mb-3">Source Account</label>
                    <Select v-model="operation.source_account" :options="dropdownAccounts" optionValue="id" placeholder="Select an account" :filter="true" :showClear="true">
                        <template #option="slotProps">
                            {{ slotProps.option.name }}
                        </template>
                        <template #value="slotProps">
                            {{ slotProps.value?.name }}
                        </template>
                    </Select>
                </div>
                <div>
                    <label for="destination_account" class="block font-bold mb-3">Destination Account</label>
                    <Select v-model="operation.destination_account" :options="dropdownAccounts" optionValue="id" placeholder="Select an account" :filter="true" :showClear="true">
                        <template #option="slotProps">
                            {{ slotProps.option.name }}
                        </template>
                        <template #value="slotProps">
                            {{ slotProps.value?.name }}
                        </template>
                    </Select>
                </div>
                <div>
                    <label for="amount" class="block font-bold mb-3">Amount</label>
                    <InputText id="amount" v-model="operation.amount" required="true" :invalid="submitted && !operation.amount" fluid />
                    <small v-if="submitted && !operation.amount" class="text-red-500">Amount is required.</small>
                </div>
                <div>
                    <label for="description" class="block font-bold mb-3">Description</label>
                    <InputText id="description" v-model="operation.description" required="true" rows="3" cols="20" fluid />
                </div>
            </div>

            <template #footer>
                <Button label="Cancel" icon="pi pi-times" text @click="hideDialog" />
                <Button label="Save" icon="pi pi-check" @click="saveoperation" />
            </template>
        </Dialog>

        <Dialog v-model:visible="deleteOperationDialog" :style="{ width: '450px' }" header="Confirm" :modal="true">
            <div class="flex items-center gap-4">
                <i class="pi pi-exclamation-triangle !text-3xl" />
                <span v-if="operation"
                    >Are you sure you want to delete <b>{{ operation.first_name }} {{ operation.last_name }}</b
                    >?</span
                >
            </div>
            <template #footer>
                <Button label="No" icon="pi pi-times" text @click="deleteoperationDialog = false" />
                <Button label="Yes" icon="pi pi-check" @click="deleteoperation" />
            </template>
        </Dialog>

        <Dialog v-model:visible="deleteoperationsDialog" :style="{ width: '450px' }" header="Confirm" :modal="true">
            <div class="flex items-center gap-4">
                <i class="pi pi-exclamation-triangle !text-3xl" />
                <span v-if="operation">Are you sure you want to delete the selected operations?</span>
            </div>
            <template #footer>
                <Button label="No" icon="pi pi-times" text @click="deleteoperationsDialog = false" />
                <Button label="Yes" icon="pi pi-check" text @click="deleteSelectedoperations" />
            </template>
        </Dialog>
    </div>
</template>
