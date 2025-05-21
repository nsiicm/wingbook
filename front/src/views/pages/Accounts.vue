<script setup>
import { FilterMatchMode } from '@primevue/core/api';
import { useToast } from 'primevue/usetoast';
import { onMounted, ref } from 'vue';
import api from '@/axios';

onMounted(() => {
    api.get('/accounts/').then((response) => (accounts.value = response.data))
    api.get('/people/').then((response) => (dropdownPeople.value = response.data))
});

const toast = useToast();
const dt = ref();
const accounts = ref();
const accountDialog = ref(false);
const deleteAccountDialog = ref(false);
const deleteaccountsDialog = ref(false);
const account = ref({});
const dropdownPeople = ref([]);
const selectedaccounts = ref();
const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS }
});
const submitted = ref(false);

function openNew() {
    account.value = {};
    submitted.value = false;
    accountDialog.value = true;
}

function hideDialog() {
    accountDialog.value = false;
    submitted.value = false;
}

function saveaccount() {
    submitted.value = true;
    if (account.value.id) {
        const index = findIndexById(account.value.id);
        accounts.value[index] = { ...accounts.value[index], ...account.value };
        api.put(`/accounts/${account.value.id}/`, account.value)
            .then(() => {
                accounts.value[index] = account.value;
                accountDialog.value = false;
                account.value = {};
                toast.add({ severity: 'success', summary: 'Successful', detail: 'AccountUpdated', life: 3000 });
            })
            .catch((error) => {
                console.error(error);
                toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to update account', life: 3000 });
            });
    } else {
        if (account.value.name || account.value.person) { // Add validation for required fields
            api.post('/accounts/', account.value)
                .then((response) => {
                    accounts.value.push(response.data); // Add the newly created account to the list
                    accountDialog.value = false;
                    account.value = {};
                    toast.add({ severity: 'success', summary: 'Successful', detail: 'AccountCreated', life: 3000 });
                })
                .catch((error) => {
                    console.error(error);
                    toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to create account', life: 3000 });
                });
        }
    }
}

function editAccount(prod) {
    account.value = { ...prod };
    accountDialog.value = true;
}

function confirmDeleteAccount(prod) {
    account.value = prod;
    deleteAccountDialog.value = true;
}

function deleteaccount() {
    api.delete(`/accounts/${account.value.id}/`)
        .then(() => {
            accounts.value = accounts.value.filter((val) => val.id !== account.value.id);
            deleteAccountDialog.value = false;
            account.value = {};
            toast.add({ severity: 'success', summary: 'Successful', detail: 'AccountDeleted', life: 3000 });
        })
        .catch((error) => {
            console.error(error);
            toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to delete account', life: 3000 });
        });
}

function findIndexById(id) {
    let index = -1;
    for (let i = 0; i < accounts.value.length; i++) {
        if (accounts.value[i].id === id) {
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
    deleteaccountsDialog.value = true;
}

function deleteSelectedaccounts() {
    accounts.value = accounts.value.filter((val) => !selectedaccounts.value.includes(val));
    deleteaccountsDialog.value = false;
    selectedaccounts.value = null;
    toast.add({ severity: 'success', summary: 'Successful', detail: 'accounts Deleted', life: 3000 });
}
</script>

<template>
    <div>
        <div class="card">
            <Toolbar class="mb-6">
                <template #start>
                    <Button label="New" icon="pi pi-plus" severity="secondary" class="mr-2" @click="openNew" />
                    <Button label="Delete" icon="pi pi-trash" severity="secondary" @click="confirmDeleteSelected"
                        :disabled="!selectedaccounts || !selectedaccounts.length" />
                </template>

                <template #end>
                    <Button label="Export" icon="pi pi-upload" severity="secondary" @click="exportCSV($event)" />
                </template>
            </Toolbar>

            <DataTable ref="dt" v-model:selection="selectedaccounts" :value="accounts" dataKey="id" :paginator="true"
                :rows="10" :filters="filters"
                paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                :rowsPerPageOptions="[5, 10, 25]"
                currentPageReportTemplate="Showing {first} to {last} of {totalRecords} accounts">
                <template #header>
                    <div class="flex flex-wrap gap-2 items-center justify-between">
                        <h4 class="m-0">Manage accounts</h4>
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
                <Column field="name" header="Account Name" sortable style="min-width: 16rem"></Column>
                <Column field="balance" header="Account Balance" sortable style="min-width: 16rem"></Column>
            </DataTable>
        </div>

        <Dialog v-model:visible="accountDialog" :style="{ width: '450px' }" header="account Details" :modal="true">
            <div class="flex flex-col gap-6">
                <img v-if="account.image" :src="`https://primefaces.org/cdn/primevue/images/account/${account.image}`"
                    :alt="account.image" class="block m-auto pb-4" />
                <div>
                    <label for="name" class="block font-bold mb-3">Account name</label>
                    <InputText id="name" v-model.trim="account.name" required="false" autofocus fluid />
                </div>
                <div>
                    <label for="person" class="block font-bold mb-3">Person linked to account</label>
                    <Dropdown v-model="account.person" :options="dropdownPeople" optionValue="id"
                        placeholder="Select a person" :filter="true" :showClear="true">
                        <template #option="slotProps">
                            {{ slotProps.option.first_name }} {{ slotProps.option.last_name }}
                        </template>
                        <template #value="slotProps">
                            {{ slotProps.value?.first_name }} {{ slotProps.value?.last_name }}
                        </template>
                    </Dropdown>
                </div>
            </div>

            <template #footer>
                <Button label="Cancel" icon="pi pi-times" text @click="hideDialog" />
                <Button label="Save" icon="pi pi-check" @click="saveaccount" />
            </template>
        </Dialog>

        <Dialog v-model:visible="deleteAccountDialog" :style="{ width: '450px' }" header="Confirm" :modal="true">
            <div class="flex items-center gap-4">
                <i class="pi pi-exclamation-triangle !text-3xl" />
                <span v-if="account">Are you sure you want to delete <b>{{ account.first_name }} {{ account.last_name
                        }}</b>?</span>
            </div>
            <template #footer>
                <Button label="No" icon="pi pi-times" text @click="deleteaccountDialog = false" />
                <Button label="Yes" icon="pi pi-check" @click="deleteaccount" />
            </template>
        </Dialog>

        <Dialog v-model:visible="deleteaccountsDialog" :style="{ width: '450px' }" header="Confirm" :modal="true">
            <div class="flex items-center gap-4">
                <i class="pi pi-exclamation-triangle !text-3xl" />
                <span v-if="account">Are you sure you want to delete the selected accounts?</span>
            </div>
            <template #footer>
                <Button label="No" icon="pi pi-times" text @click="deleteaccountsDialog = false" />
                <Button label="Yes" icon="pi pi-check" text @click="deleteSelectedaccounts" />
            </template>
        </Dialog>
    </div>
</template>
