import traceback

from model import *

def decode_dataset(model, dataset):
    logging.info('decoding [%s] set, num. examples: %d', dataset.name, dataset.count)

    decode_results = []
    cum_num = 0
    for example in dataset.examples:
        cand_list = model.decode(example, dataset.grammar, dataset.terminal_vocab,
                                 beam_size=50, max_time_step=100)

        exg_decode_results = []
        for cid, cand in enumerate(cand_list[:10]):
            try:
                ast_tree = decode_tree_to_ast(cand.tree)
                code = astor.to_source(ast_tree)
                exg_decode_results.append((cid, cand, ast_tree, code))
            except:
                print "Exception in converting tree to code:"
                print '-' * 60
                print 'raw_id: %d, beam pos: %d' % (example.raw_id, cid)
                traceback.print_exc(file=sys.stdout)
                print '-' * 60

        cum_num += 1
        if cum_num % 10 == 0:
            print '%d examples so far ...' % cum_num

        decode_results.append(exg_decode_results)

    serialize_to_file(decode_results, '%s.decode_results.profile' % dataset.name)