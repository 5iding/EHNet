from pytorch_lightning import Trainer
from pytorch_lightning.logging import TensorBoardLogger
from pytorch_lightning.callbacks import ModelCheckpoint
from model.ehnet_model import EHNetModel
from argparse import Namespace
import os

train_dir = './WAVs/dataset/training'
val_dir = './WAVs/dataset/validation'
test_dir = './WAVs/dataset/testing_seen_noise'

model = EHNetModel(hparams=Namespace(**{'train_dir': train_dir,
                                        'val_dir': val_dir,
                                        'test_dir': test_dir,
                                        'batch_size': 32,
                                        'n_frequency_bins': 256,
                                        'n_kernels': 256,
                                        'kernel_size_f': 32,
                                        'kernel_size_t': 11,
                                        'n_lstm_layers': 2,
                                        'n_lstm_units': 1024,
                                        'lstm_dropout': 0.3}))

logger = TensorBoardLogger(save_dir=os.getcwd(), name="lightning_logs")
checkpoint_path = os.path.join(logger.save_dir, logger.name, f"version_{logger.version}")
checkpoint_callback = ModelCheckpoint(filepath=checkpoint_path, verbose=1, save_top_k=5, mode='min')

trainer = Trainer(gpus=1, min_epochs=200, logger=logger, checkpoint_callback=checkpoint_callback)
trainer.fit(model)
