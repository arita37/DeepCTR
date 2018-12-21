import numpy as np
import pytest
from deepctr.models import xDeepFM
from deepctr.utils import custom_objects
from tensorflow.python.keras.models import save_model, load_model


@pytest.mark.parametrize(
    'hidden_size,cin_layer_size,cin_direct,cin_activation,sparse_feature_num',
    [((256,), (), False, 'linear', 1), ((), (256,), False, 'linear', 2), ((256,), (256,), True, 'relu', 3)
     ]
)
def test_xDeepFM(hidden_size, cin_layer_size, cin_direct, cin_activation, sparse_feature_num):
    model_name = "xDeepFM"

    sample_size = 64
    feature_dim_dict = {"sparse": {}, 'dense': []}
    for name, num in zip(["sparse", "dense"], [sparse_feature_num, sparse_feature_num]):
        if name == "sparse":
            for i in range(num):
                feature_dim_dict[name][name + '_' +
                                       str(i)] = np.random.randint(1, 10)
        else:
            for i in range(num):
                feature_dim_dict[name].append(name + '_' + str(i))
    sparse_input = [np.random.randint(0, dim, sample_size)
                    for dim in feature_dim_dict['sparse'].values()]
    dense_input = [np.random.random(sample_size)
                   for name in feature_dim_dict['dense']]

    y = np.random.randint(0, 2, sample_size)
    x = sparse_input + dense_input

    model = xDeepFM(feature_dim_dict, hidden_size=hidden_size, cin_layer_size=cin_layer_size,
                    cin_direct=cin_direct, cin_activation=cin_activation, keep_prob=0.5, )
    model.compile('adam', 'binary_crossentropy',
                  metrics=['binary_crossentropy'])
    model.fit(x, y, batch_size=100, epochs=1, validation_split=0.5)

    print(model_name+" test train valid pass!")
    model.save_weights(model_name + '_weights.h5')
    model.load_weights(model_name + '_weights.h5')
    print(model_name+" test save load weight pass!")
    save_model(model, model_name + '.h5')
    model = load_model(model_name + '.h5', custom_objects)
    print(model_name + " test save load model pass!")

    print(model_name + " test pass!")


@pytest.mark.parametrize(
    'hidden_size,cin_layer_size,',
    [((), ()), ((8,), (3, 8)),
     ]
)
def test_xDeepFM_invalid(hidden_size, cin_layer_size):
    feature_dim_dict = {'sparse': {'sparse_1': 2, 'sparse_2': 5,
                                   'sparse_3': 10}, 'dense': ['dense_1', 'dense_2', 'dense_3']}
    with pytest.raises(ValueError):
        _ = xDeepFM(feature_dim_dict, hidden_size=hidden_size,
                    cin_layer_size=cin_layer_size,)


if __name__ == "__main__":
    test_xDeepFM((256), (128,), False, 'linear')
