#-*- coding:utf-8 -*-
import torch


def from_example_list(args, ex_list, device='cpu', train=True):
    if train:
        ex_list = sorted(ex_list, key=lambda x: len(x.input_idx), reverse=True)
    batch = Batch(ex_list, device)
    pad_idx = args.pad_idx
    tag_pad_idx = args.tag_pad_idx

    batch.utt = [ex.utt for ex in ex_list]
    input_lens = [len(ex.input_idx) for ex in ex_list]
    max_len = max(input_lens)
    input_ids = [ex.input_idx + [pad_idx] * (max_len - len(ex.input_idx)) for ex in ex_list]
    batch.input_ids = torch.tensor(input_ids, dtype=torch.long, device=device)
    batch.lengths = input_lens

    batch.labels, batch.tag_ids, batch.sep_tag_ids = None, None, None
    batch.act_ids, batch.slot_ids,  = None, None
    batch.tag_mask = torch.tensor([[1] * max_len for _ in range(len(ex_list))], device=device)

    if train:
        batch.labels = [ex.slotvalue for ex in ex_list]
        tag_lens = [len(ex.tag_id) for ex in ex_list]
        max_tag_lens = max(tag_lens)

        tag_ids = [ex.tag_id + [tag_pad_idx] * (max_tag_lens - len(ex.tag_id)) for ex in ex_list]
        act_ids = [ex.act_id + [tag_pad_idx] * (max_tag_lens - len(ex.act_id)) for ex in ex_list]
        slot_ids = [ex.slot_id + [tag_pad_idx] * (max_tag_lens - len(ex.slot_id)) for ex in ex_list]
        sep_tag_ids=[ex.sep_tag_id + [tag_pad_idx] * (max_tag_lens - len(ex.sep_tag_id)) for ex in ex_list]

        tag_mask = [[1] * len(ex.tag_id) + [0] * (max_tag_lens - len(ex.tag_id)) for ex in ex_list]
        batch.tag_ids = torch.tensor(tag_ids, dtype=torch.long, device=device)
        batch.act_ids = torch.tensor(act_ids, dtype=torch.long, device=device)
        batch.slot_ids = torch.tensor(slot_ids, dtype=torch.long, device=device)
        batch.sep_tag_ids= torch.tensor(sep_tag_ids, dtype=torch.long, device=device)
        batch.tag_mask = torch.tensor(tag_mask, dtype=torch.float, device=device)

    return batch


class Batch():

    def __init__(self, examples, device):
        super(Batch, self).__init__()

        self.examples = examples
        self.device = device

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        return self.examples[idx]
