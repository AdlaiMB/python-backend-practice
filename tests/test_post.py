from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")

    # def validate(post):
    #     return schemas.PostOut(**post)
    
    # posts_map = map(validate, response.json())
    # posts_list = list(posts_map)
    
    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")

    assert response.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")

    assert response.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get("/posts/8888")

    assert response.status_code == 404

def  test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**response.json())

    assert post.Post.id == test_posts[0].id 
    assert post.Post.content == test_posts[0].content

@pytest.mark.parametrize("title, content, published", [
    ("awesome new content", "awesome new content", True), 
    ("favorite pizza", "I love pepperoni", True), 
    ("tallest skyscrapers", "wahoo", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    response = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.Post(**response.json())

    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]

def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    response = authorized_client.post("/posts/", json={"title": "randome title", "content": "random content"})

    created_post = schemas.Post(**response.json())

    assert response.status_code == 201
    assert created_post.title ==  "randome title"
    assert created_post.content ==  "random content"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]

def test_unauthorized_user_create_post(client, test_user, test_posts):
    response = client.post("/posts/", json={"title": "randome title", "content": "random content"})

    assert response.status_code == 401

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    
    assert response.status_code == 401

def test_delete_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert response.status_code == 204

def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    response = authorized_client.delete("/posts/88888")

    assert response.status_code == 404

def  test_delete_other_user_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")

    assert response.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_updated_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
     
    response = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)

    assert response.status_code == 403

def test_unauthorized_user_update_post(client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }

    response = client.put(f"/posts/{test_posts[0].id}", json=data)
    
    assert response.status_code == 401

def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }

    response = authorized_client.put("/posts/88888", json=data)

    assert response.status_code == 404