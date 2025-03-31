from pytest import mark
from httpx import AsyncClient

@mark.asyncio
async def test_experiments(client: AsyncClient):
    response = await client.post('/experiments/', json={'name': 'test'})
    assert response.status_code == 200 or response.status_code == 201
    experiment = response.json() 

    response = await client.post('/experiments/', json={'name': 'test'})
    assert response.status_code == 200 or response.status_code == 409
    
    response = await client.get(f'/experiments/{experiment['id']}/')
    assert response.status_code == 200
    experiment = response.json()
    
    assert experiment['name'] == 'test'
    response = await client.post('/experiments/', json={'name': 'other'})
    response = await client.get(f'/experiments/')
    list = response.json()
    assert len(list) == 2

    response = await client.delete(f'/experiments/{experiment['id']}/')

    response = await client.get(f'/experiments/')
    list = response.json()
    assert len(list) == 1
    response = await client.delete(f'/experiments/{experiment['id']}/')
    assert response.status_code == 404
    response = await client.get('/experiments?name=other')
    assert response.status_code == 200
    experiment = response.json()
    assert experiment['name'] == 'other'
    response = await client.patch(f'/experiments/{experiment['id']}/', json={'name': 'test'})
    
    response = await client.get('/experiments?name=test')
    assert response.status_code == 200

    response = await client.get('/experiments?name=other')
    assert response.status_code == 404
    
    response = await client.post('/experiments/', json={'name': 'test-1'})
    response = await client.post('/experiments/', json={'name': 'test-2'})
    response = await client.post('/experiments/', json={'name': 'test-3'})
    response = await client.delete('/experiments/')
    response = await client.get(f'/experiments/')
    list = response.json()
    assert len(list) == 0


@mark.asyncio
async def test_models(client: AsyncClient):
    response = await client.post('/experiments/', json={'name': 'test'})
    assert response.status_code == 200 or response.status_code == 201
    id = response.json()['id'] 

    response = await client.post(f'/experiments/{id}/models/', json={'hash':'12345' , 'name': 'llama3'}) 
    assert response.status_code == 200 or response.status_code == 201
    model = response.json() 
    
    response = await client.get(f'/models/{model['id']}/')
    model = response.json()
    assert model['hash'] == '12345'
    assert model['name'] == 'llama3'
    assert model['epoch'] == 0
    
    response = await client.patch(f'/models/{model['id']}/', json={'epoch': 15})
    assert response.status_code == 204


    response = await client.get(f'/models/{model['id']}/')
    model = response.json() 
    assert model['epoch'] == 15

    response = await client.post(f'/experiments/{id}/models/', json={'hash':'12325' , 'name': 'llama3.2'}) 
    assert response.status_code == 200 or response.status_code == 201 
    
    response = await client.post(f'/experiments/{id}/models/', json={'hash':'12325' , 'name': 'llama3.2'}) 
    assert response.status_code == 409

    response = await client.get(f'/experiments/{id}/models/')
    assert len(response.json()) == 2

    
    response = await client.delete(f'/models/{model['id']}/')
    assert response.status_code == 204


    response = await client.get(f'/experiments/{id}/models/')
    assert len(response.json()) == 1



@mark.asyncio
async def test_modules(client: AsyncClient):
    response = await client.post('/experiments/', json={'name': 'test'})
    assert response.status_code == 200 or response.status_code == 201 
    response = await client.post(f'/experiments/{response.json()['id'] }/models/', json={'hash':'12345' , 'name': 'llama3'}) 
    assert response.status_code == 200 or response.status_code == 201
    model = response.json() 
    id = model['id']
    
    response = await client.put(f'/models/{id}/modules/12345/', json={'type':'nn', 'name':'mlp', 'epoch':0, 'arguments': {'in_size':784, 'out_size':10}})
    assert response.status_code == 204

    response = await client.put(f'/models/{id}/modules/12345/', json={'type':'nn', 'name':'mlp', 'epoch':10, 'arguments': {'in_size':784, 'out_size':10}})
    assert response.status_code == 204

    response = await client.put(f'/models/{id}/modules/12346/', json={'type':'optimizer', 'name':'adam', 'epoch':10, 'arguments': {'in_size':784, 'out_size':10}})
    assert response.status_code == 204


    response = await client.get(f'/models/{id}/modules/')
    assert len(response.json()) == 2

    
    response = await client.get(f'/models/{id}/modules?type=nn')
    assert len(response.json()) == 1


@mark.asyncio
async def test_metrics(client: AsyncClient):
    response = await client.post('/experiments/', json={'name': 'test'})
    assert response.status_code == 200 or response.status_code == 201 
    response = await client.post(f'/experiments/{response.json()['id'] }/models/', json={'hash':'12345' , 'name': 'llama3'}) 
    assert response.status_code == 200 or response.status_code == 201
    model = response.json() 
    id = model['id']


    response = await client.post(f'/models/{id}/metrics/', json={'name':'accuracy', 'value':0.99, 'epoch': 1, 'phase': 'train'})
    assert response.status_code == 201
    response = await client.post(f'/models/{id}/metrics/', json={'name':'accuracy', 'value':0.99, 'epoch': 2, 'phase': 'train'})
    response = await client.get(f'/models/{id}/metrics/')

    assert len(response.json()) == 2


@mark.asyncio
async def test_iterations(client: AsyncClient):
    response = await client.post('/experiments/', json={'name': 'test'})
    assert response.status_code == 200 or response.status_code == 201 
    response = await client.post(f'/experiments/{response.json()['id'] }/models/', json={'hash':'12345' , 'name': 'llama3'}) 
    assert response.status_code == 200 or response.status_code == 201
    model = response.json() 
    id = model['id']
    response = await client.get(f'/experiments/{id}/iterations/')
    assert len(response.json()) == 1